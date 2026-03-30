#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证相关性能测试场景
"""

from locust import HttpUser, task, between
import json
import random
import time
import logging
from config import TestConfig

logger = logging.getLogger(__name__)

class AuthTestUser(HttpUser):
    """认证功能性能测试用户"""
    
    wait_time = between(1, 2)
    
    def on_start(self):
        """测试开始时执行"""
        self.token = None
        self.user_data = None
    
    @task(5)
    def login_test(self):
        """登录性能测试"""
        user_data = random.choice(TestConfig.TEST_USERS)
        
        with self.client.post("/api/auth/login", 
                            json={
                                "phone": user_data["phone"],
                                "password": user_data["password"]
                            },
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        self.token = result.get("data", {}).get("token")
                        response.success()
                    else:
                        response.failure(f"登录失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("登录响应JSON解析失败")
            else:
                response.failure(f"登录请求失败: {response.status_code}")
    
    @task(2)
    def register_test(self):
        """注册性能测试"""
        # 生成随机用户数据
        timestamp = int(time.time())
        phone = f"138{timestamp % 100000000:08d}"
        
        register_data = {
            "username": f"test_user_{timestamp}",
            "phone": phone,
            "password": "123456",
            "realName": "测试用户",
            "idCard": f"31010119900101{timestamp % 10000:04d}",
            "userType": random.choice(["PASSENGER", "DRIVER"])
        }
        
        with self.client.post("/api/auth/register",
                            json=register_data,
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        response.success()
                    else:
                        # 手机号已存在等情况也算正常
                        if "已存在" in result.get("message", ""):
                            response.success()
                        else:
                            response.failure(f"注册失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("注册响应JSON解析失败")
            else:
                response.failure(f"注册请求失败: {response.status_code}")
    
    @task(1)
    def logout_test(self):
        """登出性能测试"""
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with self.client.post("/api/auth/logout",
                            headers=headers,
                            catch_response=True) as response:
            if response.status_code == 200:
                self.token = None
                response.success()
            else:
                response.failure(f"登出请求失败: {response.status_code}")
    
    @task(1)
    def refresh_token_test(self):
        """刷新令牌性能测试"""
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with self.client.post("/api/auth/refresh",
                            headers=headers,
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        new_token = result.get("data", {}).get("token")
                        if new_token:
                            self.token = new_token
                        response.success()
                    else:
                        response.failure(f"刷新令牌失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("刷新令牌响应JSON解析失败")
            else:
                response.failure(f"刷新令牌请求失败: {response.status_code}")


class ConcurrentLoginUser(HttpUser):
    """并发登录测试用户"""
    
    wait_time = between(0.5, 1)
    
    @task
    def concurrent_login(self):
        """并发登录测试"""
        user_data = random.choice(TestConfig.TEST_USERS)
        
        start_time = time.time()
        
        with self.client.post("/api/auth/login",
                            json={
                                "phone": user_data["phone"],
                                "password": user_data["password"]
                            },
                            catch_response=True) as response:
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        # 记录响应时间
                        if response_time > 1000:  # 超过1秒
                            logger.warning(f"登录响应时间过长: {response_time:.2f}ms")
                        response.success()
                    else:
                        response.failure(f"登录失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("登录响应JSON解析失败")
            else:
                response.failure(f"登录请求失败: {response.status_code}")


class InvalidAuthUser(HttpUser):
    """无效认证测试用户"""
    
    wait_time = between(1, 3)
    
    @task(3)
    def invalid_login_test(self):
        """无效登录测试"""
        invalid_credentials = [
            {"phone": "13800138000", "password": "wrong_password"},
            {"phone": "invalid_phone", "password": "123456"},
            {"phone": "", "password": "123456"},
            {"phone": "13800138000", "password": ""},
            {"phone": "13800138999", "password": "123456"},  # 不存在的用户
        ]
        
        cred = random.choice(invalid_credentials)
        
        with self.client.post("/api/auth/login",
                            json=cred,
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") != 200:
                        # 预期的失败响应
                        response.success()
                    else:
                        response.failure("无效凭据不应该登录成功")
                except json.JSONDecodeError:
                    response.failure("登录响应JSON解析失败")
            elif response.status_code == 400 or response.status_code == 401:
                # 预期的错误状态码
                response.success()
            else:
                response.failure(f"意外的响应状态码: {response.status_code}")
    
    @task(2)
    def invalid_register_test(self):
        """无效注册测试"""
        invalid_data_list = [
            # 缺少必填字段
            {"phone": "13800138000"},
            # 无效手机号
            {"phone": "123", "password": "123456", "username": "test"},
            # 密码太短
            {"phone": "13800138000", "password": "123", "username": "test"},
            # 无效身份证
            {"phone": "13800138000", "password": "123456", "username": "test", "idCard": "123"},
        ]
        
        data = random.choice(invalid_data_list)
        
        with self.client.post("/api/auth/register",
                            json=data,
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") != 200:
                        # 预期的失败响应
                        response.success()
                    else:
                        response.failure("无效数据不应该注册成功")
                except json.JSONDecodeError:
                    response.failure("注册响应JSON解析失败")
            elif response.status_code == 400:
                # 预期的错误状态码
                response.success()
            else:
                response.failure(f"意外的响应状态码: {response.status_code}")
    
    @task(1)
    def unauthorized_access_test(self):
        """未授权访问测试"""
        protected_endpoints = [
            "/api/user/profile",
            "/api/trips/my",
            "/api/bookings/my",
            "/api/admin/users"
        ]
        
        endpoint = random.choice(protected_endpoints)
        
        with self.client.get(endpoint, catch_response=True) as response:
            if response.status_code == 401 or response.status_code == 403:
                # 预期的未授权响应
                response.success()
            else:
                response.failure(f"未授权访问应该返回401/403，实际: {response.status_code}")


class AuthStressUser(HttpUser):
    """认证压力测试用户"""
    
    wait_time = between(0.1, 0.5)  # 更短的等待时间
    
    def on_start(self):
        """开始时登录"""
        self.login()
    
    def login(self):
        """登录"""
        user_data = random.choice(TestConfig.TEST_USERS)
        
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    @task
    def rapid_api_calls(self):
        """快速API调用"""
        if not hasattr(self, 'token') or not self.token:
            self.login()
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 快速调用多个API
        endpoints = [
            "/api/user/profile",
            "/api/trips/search?startLocation=上海&endLocation=北京",
            "/api/bookings/my"
        ]
        
        endpoint = random.choice(endpoints)
        
        with self.client.get(endpoint, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                # Token可能过期，重新登录
                self.login()
                response.success()
            else:
                response.failure(f"API调用失败: {response.status_code}") 