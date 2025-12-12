#!/usr/bin/env python3
"""
MCP服务综合测试脚本
测试整个MCP摄像头服务的功能
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera_service import CameraService
from image_analyzer import ImageAnalyzer


async def test_mcp_service():
    """测试MCP服务的完整功能"""
    print("正在测试MCP摄像头服务的完整功能...")
    
    # 测试摄像头服务
    print("\n1. 测试摄像头服务...")
    camera_service = CameraService()
    
    if not camera_service.open_camera(0):
        print("错误: 无法打开摄像头")
        return False
    
    print("✓ 摄像头已成功打开")
    
    # 捕获图像
    image_base64 = camera_service.capture_image_base64()
    if image_base64 is None:
        print("错误: 无法捕获图像")
        camera_service.close_camera()
        return False
    
    print("✓ 成功捕获图像并编码为Base64")
    camera_service.close_camera()
    
    # 测试图像分析服务
    print("\n2. 测试图像分析服务...")
    analyzer = ImageAnalyzer()
    
    analysis_result = analyzer.analyze_image_from_base64(image_base64)
    if analysis_result is None:
        print("错误: 图像分析失败")
        return False
    
    print("✓ 图像分析成功")
    print(f"  图像尺寸: {analysis_result['dimensions']['width']}x{analysis_result['dimensions']['height']}")
    print(f"  平均亮度: {analysis_result['brightness']:.2f}")
    
    # 测试文本格式分析结果
    text_result = analyzer.get_basic_analysis(image_base64)
    print("\n3. 图像分析结果:")
    print(text_result)
    
    return True


async def main():
    """主函数"""
    try:
        success = await test_mcp_service()
        if success:
            print("\n🎉 MCP摄像头服务综合测试成功!")
            return 0
        else:
            print("\n❌ MCP摄像头服务综合测试失败!")
            return 1
    except Exception as e:
        print(f"\n测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)