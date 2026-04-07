from dataclasses import dataclass
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime
import os
from dotenv import load_dotenv


load_dotenv()
checkpointer = InMemorySaver()


@dataclass
class Context:
    """自定义运行时上下文模式。"""
    user_id: str


@dataclass
class ResponseFormat:
    """代理的响应模式。"""
    # 带双关语的回应（始终必需）
    punny_response: str
    # 天气的任何有趣信息（如果有）
    weather_conditions: str | None = None


@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city}总是阳光明媚！"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 获取用户信息。"""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


SYSTEM_PROMPT = """你是一位擅长用双关语表达的专家天气预报员。

你可以使用两个工具：

- get_weather_for_location：用于获取特定地点的天气
- get_user_location：用于获取用户的位置

如果用户询问天气，请确保你知道具体位置。如果从问题中可以判断他们指的是自己所在的位置，请使用 get_user_location 工具来查找他们的位置。"""

# 创建带认证的模型实例（使用 OpenRouter）
llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL_NAME"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    max_tokens=8192,  # 限制最大 token 数，避免超出 credits 限制（根据当前 credits 调整）

)

# `thread_id` 是给定对话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}

agent = create_agent(
    model=llm,
    tools=[get_weather_for_location, get_user_location],
    system_prompt=SYSTEM_PROMPT,
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer,
)

# 运行代理并获取结果
result = agent.invoke(
    {"messages": [{"role": "user", "content": "外面的天气怎么样？"}]},
    config=config,
    context=Context(user_id="1"),
)

# 打印输出结果
print("=" * 50)
print("Agent 响应:")
print("=" * 50)
print(result['structured_response'])
print("=" * 50)

# 如果需要查看更详细的信息，可以访问具体的消息内容
if isinstance(result, dict) and "messages" in result:
    messages = result.get("messages")
    for msg in messages:

        print(f"\n角色：{msg.type if hasattr(msg, 'type') else 'unknown'}")
        print(f"内容：{msg.content}")
        print(f'全部内容：{msg}')

