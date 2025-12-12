#!/usr/bin/env python3
"""
简单的摄像头测试脚本
用于验证摄像头功能是否正常工作
"""

import cv2
import sys

def test_camera():
    """测试摄像头功能"""
    print("正在测试摄像头...")
    
    # 尝试打开默认摄像头
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("错误: 无法打开摄像头")
        return False
    
    print("摄像头已打开，正在捕获图像...")
    
    # 捕获一帧图像
    ret, frame = cap.read()
    
    if not ret:
        print("错误: 无法从摄像头读取图像")
        cap.release()
        return False
    
    # 获取图像信息
    height, width, channels = frame.shape
    print(f"成功捕获图像: {width}x{height}, {channels}通道")
    
    # 保存图像用于验证
    cv2.imwrite("test_capture.jpg", frame)
    print("图像已保存为 test_capture.jpg")
    
    # 释放摄像头
    cap.release()
    print("摄像头测试完成")
    
    return True

if __name__ == "__main__":
    try:
        success = test_camera()
        if success:
            print("摄像头测试成功!")
            sys.exit(0)
        else:
            print("摄像头测试失败!")
            sys.exit(1)
    except Exception as e:
        print(f"测试过程中发生异常: {e}")
        sys.exit(1)