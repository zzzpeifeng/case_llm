import json
import os

from openai import OpenAI


from dotenv import load_dotenv
load_dotenv()

# 初始化客户端 (需要提前设置环境变量 OPENAI_API_KEY，或在此处传入)
client = OpenAI(api_key=os.getenv("Z_API_KEY"),
                base_url=os.getenv("Z_BASE_URL"))


# 2. 定义 Agent 可以使用的“工具库”
# 模拟工具库
def get_phone_stock(model_name):
    print(f"🔍 [工具执行] 查询 {model_name} 库存...")
    return "有货" if "14" in model_name else "缺货"


def place_order(model_name):
    print(f"📦 [工具执行] 为 {model_name} 下单成功！")
    return "订单号：MI-123456"


# 简化的工具描述
tools = [
    {"type": "function",
     "function": {
         "name": "get_phone_stock",
         "parameters": {
             "type": "object",
             "properties": {
                 "model_name": {"type": "string"}
             }
         }
     }
     },
    {"type": "function", "function": {"name": "place_order", "parameters": {"type": "object", "properties": {
        "model_name": {"type": "string"}}}}}
]


def run_agent(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]

    # 💥 核心：设置最大思考步数，防止无限循环
    max_turns = 5

    for i in range(max_turns):
        print(f"Thoughts: {messages}"f"[{i + 1}/{max_turns}] 🤔 模型正在思考...")
        response = client.chat.completions.create(
            model=os.getenv("Z_MODEL"),
            messages=messages,
            tools=tools,
            max_tokens=11843
        )

        message = response.choices[0].message
        messages.append(message)  # 记录模型当下的想法

        # 如果模型不再需要调用工具，说明它思考完了，返回最终结果
        if not message.tool_calls:
            return message.content

        # 如果有工具调用，依次执行
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            # 路由到具体的函数
            if func_name == "get_phone_stock":
                result = get_phone_stock(args['model_name'])
            elif func_name == "place_order":
                result = place_order(args['model_name'])

            # 将“观察”到的结果喂回给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "达到最大思考步数，未能完成任务。"


print(f"🤖 最终回复：{run_agent('我想买一台 Xiaomi 14')}")
