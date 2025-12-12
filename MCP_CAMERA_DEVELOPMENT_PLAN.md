# MCP Camera 工具服务开发规划

## 项目概述

本项目旨在开发一个基于MCP(Model Context Protocol)框架的摄像头工具服务，允许AI助手访问和控制网络摄像头，捕获图像并进行分析处理。该工具将集成到Cherry studio等AI系统中，为AI提供视觉输入能力。

## 技术架构

### 核心技术栈
- **编程语言**: Python 3.14+
- **主要框架**: MCP (Model Context Protocol) v1.23.3
- **摄像头处理库**: OpenCV
- **依赖管理**: uv 包管理器
- **项目配置**: pyproject.toml

### 项目结构
```
mcp_camera/
├── main.py              # 程序入口点
├── camera_service.py    # 摄像头服务核心实现
├── image_analyzer.py    # 图像分析模块
├── mcp_handlers.py      # MCP协议处理器
├── pyproject.toml       # 项目配置文件
├── uv.lock             # 依赖锁定文件
└── README.md           # 项目说明文档
```

## 功能需求

### 核心功能
1. **摄像头连接管理**
   - 打开/关闭摄像头连接
   - 支持多个摄像头设备
   - 自动检测可用摄像头

2. **图像捕获功能**
   - 单张图片快速捕获
   - 连续图像捕获（视频流）
   - 可调节分辨率和帧率

3. **摄像头设置调整**
   - 调整亮度、对比度、饱和度
   - 设置分辨率和帧率
   - 白平衡和其他高级参数

4. **基础图像处理**
   - 图像翻转（水平/垂直）
   - 图像旋转
   - 基础滤镜效果

5. **图像分析能力**
   - 物体识别（基础）
   - 面部检测
   - 文字识别（OCR）
   - 场景分类

### MCP接口功能
1. **工具定义**
   - `capture_image`: 捕获单张图片
   - `start_video_stream`: 开始视频流传输
   - `stop_video_stream`: 停止视频流传输
   - `adjust_camera_settings`: 调整摄像头参数
   - `analyze_image`: 分析图像内容

2. **资源定义**
   - 提供捕获的图像资源
   - 提供实时视频流资源

## 详细设计

### 1. 依赖配置 (pyproject.toml)
需要在现有基础上增加必要的依赖项：
```toml
[project]
name = "mcp-camera"
version = "0.1.0"
description = "MCP Camera Tool - 让AI具备视觉能力"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "mcp[cli]>=1.23.3",
    "opencv-python>=4.10.0",
    "numpy>=1.26.0",
    "pillow>=10.0.0",
]

[project.scripts]
mcp-camera = "main:main"
```

### 2. 主程序入口 (main.py)
```python
import asyncio
from mcp import StdioServerParameters
from camera_service import CameraService
from mcp_handlers import create_camera_tool

async def main():
    """MCP Camera服务主入口"""
    camera_service = CameraService()
    camera_tool = create_camera_tool(camera_service)
    
    # 初始化MCP服务器
    server_params = StdioServerParameters(
        tools=[camera_tool],
        resources=[]
    )
    
    # 启动服务
    await server_params.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. 摄像头服务核心 (camera_service.py)
```python
import cv2
import numpy as np
from typing import Optional, Tuple

class CameraService:
    """摄像头服务核心类"""
    
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_open = False
        
    def open_camera(self, device_index: int = 0) -> bool:
        """打开摄像头"""
        if self.is_open:
            return True
            
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            return False
            
        self.is_open = True
        return True
    
    def close_camera(self) -> None:
        """关闭摄像头"""
        if self.cap and self.is_open:
            self.cap.release()
            self.is_open = False
    
    def capture_image(self) -> Optional[np.ndarray]:
        """捕获单张图片"""
        if not self.is_open or not self.cap:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        return frame
    
    def adjust_settings(self, brightness: Optional[int] = None, 
                       contrast: Optional[int] = None) -> bool:
        """调整摄像头设置"""
        if not self.is_open or not self.cap:
            return False
            
        if brightness is not None:
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
            
        if contrast is not None:
            self.cap.set(cv2.CAP_PROP_CONTRAST, contrast)
            
        return True
```

### 4. MCP处理器 (mcp_handlers.py)
```python
from mcp import Tool
from camera_service import CameraService

def create_camera_tool(camera_service: CameraService) -> Tool:
    """创建摄像头工具"""
    
    async def capture_image_impl(params: dict) -> dict:
        """捕获图像实现"""
        device_index = params.get("device_index", 0)
        
        # 打开摄像头
        if not camera_service.open_camera(device_index):
            return {"error": "无法打开摄像头"}
            
        # 捕获图像
        image = camera_service.capture_image()
        if image is None:
            return {"error": "图像捕获失败"}
            
        # 关闭摄像头
        camera_service.close_camera()
        
        # 返回图像信息（实际应用中会返回图像数据或保存路径）
        return {
            "success": True,
            "image_size": image.shape,
            "message": f"成功捕获图像，尺寸: {image.shape}"
        }
    
    # 定义工具
    return Tool(
        name="capture_image",
        description="从指定摄像头捕获一张图片",
        parameters={
            "type": "object",
            "properties": {
                "device_index": {
                    "type": "integer",
                    "description": "摄像头设备索引，默认为0"
                }
            }
        },
        handler=capture_image_impl
    )
```

## 开发阶段计划

### 第一阶段：基础环境搭建（已完成）
- [x] 创建项目结构
- [x] 配置pyproject.toml
- [x] 设置依赖管理（uv）

### 第二阶段：核心功能实现
- [ ] 实现摄像头连接管理
- [ ] 实现图像捕获功能
- [ ] 实现基本图像处理
- [ ] 添加错误处理机制

### 第三阶段：MCP集成
- [x] 实现MCP工具定义
- [x] 实现MCP资源定义
- [x] 使用FastMCP框架和@mcp.tool装饰器
- [x] 通过stdio协议通信
- [ ] 测试与AI系统的集成(这个告诉我，我手动测试)

### 第四阶段：高级功能
- [ ] 图像分析能力集成
- [ ] 视频流支持
- [ ] 多摄像头支持
- [ ] 性能优化

## 部署与使用

### 安装步骤
1. 克隆项目仓库
2. 安装依赖：`uv sync`
3. 运行服务：`python main.py`


## 注意事项

1. **权限问题**: 在macOS上可能需要授予终端摄像头访问权限
2. **兼容性**: 不同操作系统下的摄像头API可能存在差异
3. **性能考虑**: 高分辨率图像处理可能消耗较多资源
4. **安全性**: 图像数据传输需要注意隐私保护

## 扩展建议

1. 支持更多图像分析模型（如YOLO、OCR等）
2. 添加图像存储和检索功能
3. 实现远程摄像头支持
4. 添加Web界面用于调试和监控