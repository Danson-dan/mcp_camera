import asyncio
import logging
from mcp import types
from mcp.server.fastmcp import FastMCP, Context
from camera_service import CameraService
from image_analyzer import ImageAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

camera_service = CameraService()
analyzer = ImageAnalyzer()

# 创建FastMCP服务器
mcp = FastMCP("mcp-camera")

@mcp.tool(
    name="capture_and_analyze_image",
    description="从指定摄像头捕获一张图片并返回分析结果"
)
async def capture_and_analyze_image(
    device_index: int = 0,
    ctx: Context = None
) -> str:
    """捕获摄像头图像并返回分析结果"""
    logger.info(f"正在尝试打开摄像头，设备索引: {device_index}")
    
    # 打开摄像头
    if not camera_service.open_camera(device_index):
        error_msg = "无法打开摄像头"
        logger.error(error_msg)
        return error_msg
        
    # 捕获图像
    image_base64 = camera_service.capture_image_base64()
    if image_base64 is None:
        camera_service.close_camera()
        error_msg = "图像捕获失败"
        logger.error(error_msg)
        return error_msg
        
    # 关闭摄像头
    camera_service.close_camera()
    
    # 分析图像
    analysis_result = analyzer.get_basic_analysis(image_base64)
    logger.info("成功捕获并分析图像")
    return analysis_result

async def main():
    """MCP Camera服务主入口"""
    logger.info("MCP Camera服务启动中...")
    logger.info("提供的功能: capture_and_analyze_image - 从指定摄像头捕获一张图片并返回分析结果")
    logger.info("使用stdio协议运行服务")
    
    # 使用stdio协议运行服务器
    await mcp.run_stdio_async()

if __name__ == "__main__":
    logger.info("正在启动MCP Camera服务...")
    asyncio.run(main())
