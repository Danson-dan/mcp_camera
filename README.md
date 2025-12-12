# MCP Camera Tool

MCP Camera Tool 是一个基于MCP(Model Context Protocol)框架的摄像头工具服务，允许AI助手访问和控制网络摄像头，捕获图像并进行分析处理。

## 功能特性

- 摄像头连接管理（打开/关闭）
- 图像捕获功能
- 摄像头参数调整（亮度、对比度等）
- 基础图像处理
- 图像内容分析（亮度、颜色分布、边缘检测等）
- MCP协议集成

## 技术栈

- Python 3.14+
- MCP (Model Context Protocol) v1.23.3
- OpenCV for camera operations
- uv 包管理器
- FastMCP框架

## 安装步骤

1. 克隆项目仓库
2. 安装依赖：
   ```bash
   uv sync
   ```

## 运行服务

使用uv运行MCP摄像头服务：

```bash
uv run mcp-camera
```

或者直接运行主程序：

```bash
uv run python main.py
```

## 权限说明

在macOS上，首次运行时可能需要授予终端应用程序摄像头访问权限：
1. 打开系统偏好设置
2. 进入"安全性与隐私"
3. 在"隐私"标签页中选择"相机"
4. 勾选您正在使用的终端应用程序

## 测试摄像头功能

可以运行单独的测试脚本来验证摄像头是否正常工作：

```bash
uv run python test_camera.py
```

## 与AI系统集成

要将此工具集成到支持MCP的AI系统（如Claude）中，请参考相应系统的文档配置MCP服务。

服务启动时会显示相关信息：
- 使用FastMCP框架实现
- 通过stdio协议通信
- 提供capture_and_analyze_image工具用于捕获并分析摄像头图像

## 项目结构

```
mcp_camera/
├── main.py              # 程序入口点
├── camera_service.py    # 摄像头服务核心实现
├── image_analyzer.py    # 图像分析服务
├── test_camera.py       # 摄像头测试脚本
├── test_image_analyzer.py # 图像分析器测试脚本
├── pyproject.toml       # 项目配置文件
├── uv.lock             # 依赖锁定文件
└── README.md           # 项目说明文档
```