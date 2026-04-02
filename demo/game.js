// 获取方块元素
const box = document.getElementById('box');

// 方块尺寸
const boxSize = 60;

// 初始化方块位置（屏幕中央）
let boxX = window.innerWidth / 2 - boxSize / 2;
let boxY = window.innerHeight / 2 - boxSize / 2;

// 设置初始位置
box.style.left = boxX + 'px';
box.style.top = boxY + 'px';

// 鼠标移动事件监听
document.addEventListener('mousemove', (e) => {
    // 获取鼠标位置
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    
    // 计算方块位置（使方块中心对准鼠标位置）
    boxX = mouseX - boxSize / 2;
    boxY = mouseY - boxSize / 2;
    
    // 更新方块位置
    box.style.left = boxX + 'px';
    box.style.top = boxY + 'px';
    
    // 添加轻微的缩放效果
    box.style.transform = 'scale(1.05)';
});

// 鼠标离开窗口时恢复大小
document.addEventListener('mouseleave', () => {
    box.style.transform = 'scale(1)';
});

// 窗口大小改变时调整位置
window.addEventListener('resize', () => {
    // 确保方块不会超出屏幕边界
    if (boxX > window.innerWidth - boxSize) {
        boxX = window.innerWidth - boxSize;
        box.style.left = boxX + 'px';
    }
    if (boxY > window.innerHeight - boxSize) {
        boxY = window.innerHeight - boxSize;
        box.style.top = boxY + 'px';
    }
});