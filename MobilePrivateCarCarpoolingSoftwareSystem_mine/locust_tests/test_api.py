#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 API 测试脚本
用于验证后端服务是否正常工作
"""

import requests
import json

def test_api():
    """测试 API 连接"""
    base_url = "http://localhost:8888"
    
    print("🔍 测试后端 API 连接...")
    
    # 1. 测试服务器连接
    try:
        response = requests.get(f"{base_url}/api/user/types", timeout=5)
        print(f"✅ 服务器连接成功: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应内容: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False
    
    # 2. 测试用户登录
    print("\n🔐 测试用户登录...")
    login_data = {
        "phone": "13800000001",  # zhangsan
        "password": "e10adc3949ba59abbe56e057f20f883e"  # 123456 的 MD5
    }
    
    try:
        response = requests.post(f"{base_url}/api/user/login", 
                               json=login_data, 
                               timeout=5)
        print(f"   登录请求状态: {response.status_code}")
        print(f"   响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                print("✅ 登录成功")
                user_info = result.get("data")
                print(f"   用户信息: {user_info}")
                return True
            else:
                print(f"❌ 登录失败: {result.get('msg', '未知错误')}")
        else:
            print(f"❌ 登录请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 登录请求异常: {e}")
    
    # 3. 测试行程搜索
    print("\n🔍 测试行程搜索...")
    search_params = {
        "startLng": 116.397128,
        "startLat": 39.916527,
        "endLng": 116.326419,
        "endLat": 39.896927,
        "departureTime": "2025-06-17"
    }
    
    try:
        response = requests.get(f"{base_url}/api/trip/search", 
                              params=search_params, 
                              timeout=5)
        print(f"   搜索请求状态: {response.status_code}")
        print(f"   响应内容: {response.text}")
        
        if response.status_code == 200:
            trips = response.json()
            print(f"✅ 搜索成功，找到 {len(trips) if isinstance(trips, list) else 0} 个行程")
        else:
            print(f"❌ 搜索请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 搜索请求异常: {e}")
    
    return False

if __name__ == "__main__":
    test_api() 