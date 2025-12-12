#!/usr/bin/env python3
"""
图像分析服务
提供基本的图像分析功能
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
import base64
import logging

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """图像分析服务类"""
    
    def __init__(self):
        pass
    
    def analyze_brightness(self, image: np.ndarray) -> float:
        """分析图像亮度"""
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 计算平均亮度
        brightness = np.mean(gray)
        return float(brightness)
    
    def analyze_color_distribution(self, image: np.ndarray) -> Dict[str, float]:
        """分析图像颜色分布"""
        # 分离颜色通道
        b, g, r = cv2.split(image)
        
        # 计算各通道平均值
        color_dist = {
            "red_mean": float(np.mean(r)),
            "green_mean": float(np.mean(g)),
            "blue_mean": float(np.mean(b))
        }
        
        return color_dist
    
    def detect_edges(self, image: np.ndarray) -> int:
        """检测图像边缘数量"""
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 应用Canny边缘检测
        edges = cv2.Canny(gray, 50, 150)
        # 计算边缘像素数量
        edge_count = np.sum(edges > 0)
        return int(edge_count)
    
    def analyze_image_from_base64(self, image_base64: str) -> Optional[Dict[str, Any]]:
        """从Base64编码的图像数据进行分析"""
        try:
            # 解码Base64图像
            image_data = base64.b64decode(image_base64)
            # 转换为numpy数组
            nparr = np.frombuffer(image_data, np.uint8)
            # 解码图像
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                logger.error("无法解码图像数据")
                return None
            
            # 执行各种分析
            analysis_result = {
                "dimensions": {
                    "width": image.shape[1],
                    "height": image.shape[0],
                    "channels": image.shape[2] if len(image.shape) > 2 else 1
                },
                "brightness": self.analyze_brightness(image),
                "color_distribution": self.analyze_color_distribution(image),
                "edge_count": self.detect_edges(image)
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"图像分析过程中发生错误: {e}")
            return None
    
    def get_basic_analysis(self, image_base64: str) -> str:
        """获取图像的基本分析结果（文本格式）"""
        analysis = self.analyze_image_from_base64(image_base64)
        
        if analysis is None:
            return "图像分析失败"
        
        # 格式化分析结果
        result = f"""图像分析结果:
尺寸: {analysis['dimensions']['width']}x{analysis['dimensions']['height']}
亮度: {analysis['brightness']:.2f}
颜色分布:
  - 红色平均值: {analysis['color_distribution']['red_mean']:.2f}
  - 绿色平均值: {analysis['color_distribution']['green_mean']:.2f}
  - 蓝色平均值: {analysis['color_distribution']['blue_mean']:.2f}
边缘数量: {analysis['edge_count']}"""
        
        return result