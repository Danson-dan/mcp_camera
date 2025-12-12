#!/usr/bin/env python3
"""
MCP客户端测试脚本
用于测试MCP摄像头服务是否正常工作
"""

import asyncio
import json
import sys
from mcp import StdioServerParameters, stdio_client
from mcp.types import InitializeRequest, InitializeRequestParams, ClientCapabilities, Implementation


async def test_mcp_camera_service():
    """测试MCP摄像头服务"""
    print("正在测试MCP摄像头服务...")
    
    # 创建服务器参数 - 运行我们的摄像头服务
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "main.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            print("已连接到MCP摄像头服务")
            
            # 发送初始化请求
            init_request = InitializeRequest(
                method="initialize",
                params=InitializeRequestParams(
                    protocolVersion="2024-01-01",
                    capabilities=ClientCapabilities(),
                    clientInfo=Implementation(name="test-client", version="1.0.0")
                )
            )
            
            # 发送请求
            await write_stream.send(init_request)
            print("已发送初始化请求")
            
            # 等待响应
            response = await read_stream.receive()
            print(f"收到初始化响应: {response}")
            
            # TODO: 发送list_tools请求获取可用工具
            # TODO: 发送call_tool请求调用capture_image工具
            
    except Exception as e:
        print(f"测试过程中发生异常: {e}")
        return False
        
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_mcp_camera_service())
        if success:
            print("MCP摄像头服务测试成功!")
            sys.exit(0)
        else:
            print("MCP摄像头服务测试失败!")
            sys.exit(1)
    except Exception as e:
        print(f"测试过程中发生异常: {e}")
        sys.exit(1)