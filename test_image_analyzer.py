#!/usr/bin/env python3
"""
图像分析器测试脚本
测试ImageAnalyzer类的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_analyzer import ImageAnalyzer
import cv2
import base64
import numpy as np


def create_test_image():
    """创建一个测试图像"""
    # 创建一个彩色测试图像
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 添加一些颜色区域
    img[100:200, 100:300] = [255, 0, 0]  # 红色区域
    img[200:300, 200:400] = [0, 255, 0]  # 绿色区域
    img[300:400, 300:500] = [0, 0, 255]  # 蓝色区域
    
    # 添加一些边缘
    cv2.rectangle(img, (50, 50), (590, 430), (255, 255, 255), 2)
    
    return img


def test_image_analyzer():
    """测试图像分析器"""
    print("正在测试图像分析器...")
    
    # 创建图像分析器实例
    analyzer = ImageAnalyzer()
    
    # 创建测试图像
    test_img = create_test_image()
    
    # 将图像编码为Base64
    _, buffer = cv2.imencode('.jpg', test_img)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    print("测试图像已创建并编码")
    
    # 分析图像
    print("正在分析图像...")
    analysis_result = analyzer.analyze_image_from_base64(image_base64)
    
    if analysis_result is None:
        print("错误: 图像分析失败")
        return False
    
    print("图像分析成功:")
    print(f"  尺寸: {analysis_result['dimensions']['width']}x{analysis_result['dimensions']['height']}")
    print(f"  亮度: {analysis_result['brightness']:.2f}")
    print(f"  颜色分布:")
    print(f"    红色平均值: {analysis_result['color_distribution']['red_mean']:.2f}")
    print(f"    绿色平均值: {analysis_result['color_distribution']['green_mean']:.2f}")
    print(f"    蓝色平均值: {analysis_result['color_distribution']['blue_mean']:.2f}")
    print(f"  边缘数量: {analysis_result['edge_count']}")
    
    # 测试文本格式分析结果
    print("\n测试文本格式分析结果:")
    text_result = analyzer.get_basic_analysis(image_base64)
    print(text_result)
    
    return True


if __name__ == "__main__":
    try:
        success = test_image_analyzer()
        if success:
            print("\n图像分析器测试成功!")
            sys.exit(0)
        else:
            print("\n图像分析器测试失败!")
            sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)