#!/usr/bin/env python3
"""
摄像头服务测试脚本
专门测试CameraService类的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera_service import CameraService
import cv2


def test_camera_service():
    """测试CameraService类"""
    print("正在测试CameraService类...")
    
    # 创建摄像头服务实例
    camera_service = CameraService()
    
    # 测试打开摄像头
    print("正在尝试打开摄像头...")
    if not camera_service.open_camera(0):
        print("错误: 无法打开摄像头")
        return False
    
    print("摄像头已成功打开")
    
    # 测试捕获图像
    print("正在捕获图像...")
    image = camera_service.capture_image()
    
    if image is None:
        print("错误: 无法捕获图像")
        camera_service.close_camera()
        return False
    
    print(f"成功捕获图像，尺寸: {image.shape}")
    
    # 测试保存图像
    cv2.imwrite("camera_service_test.jpg", image)
    print("图像已保存为 camera_service_test.jpg")
    
    # 测试关闭摄像头
    camera_service.close_camera()
    print("摄像头已关闭")
    
    return True


if __name__ == "__main__":
    try:
        success = test_camera_service()
        if success:
            print("CameraService测试成功!")
            sys.exit(0)
        else:
            print("CameraService测试失败!")
            sys.exit(1)
    except Exception as e:
        print(f"测试过程中发生异常: {e}")
        sys.exit(1)