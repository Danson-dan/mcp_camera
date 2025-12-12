import cv2
import numpy as np
from typing import Optional, Tuple
import base64


class CameraService:
    """摄像头服务核心类"""
    
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_open = False
        
    def open_camera(self, device_index: int = 0) -> bool:
        """打开摄像头"""
        if self.is_open:
            return True
            
        # 尝试打开摄像头
        self.cap = cv2.VideoCapture(device_index)
        
        # 如果默认方式失败，尝试其他API
        if not self.cap.isOpened():
            self.cap.release()
            # 尝试使用AVFoundation backend (macOS)
            self.cap = cv2.VideoCapture(device_index, cv2.CAP_AVFOUNDATION)
            
        # 如果AVFoundation也失败，尝试其他后端
        if not self.cap.isOpened():
            self.cap.release()
            # 尝试使用不同参数
            self.cap = cv2.VideoCapture(device_index + cv2.CAP_ANY)
            
        if not self.cap.isOpened():
            return False
            
        # 设置一些默认参数以提高兼容性
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
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
    
    def capture_image_base64(self) -> Optional[str]:
        """捕获单张图片并返回Base64编码"""
        image = self.capture_image()
        if image is None:
            return None
            
        # 将图像编码为JPEG格式
        _, buffer = cv2.imencode('.jpg', image)
        # 转换为Base64字符串
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text
    
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