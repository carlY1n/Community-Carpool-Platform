#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行程相关性能测试场景
"""

from locust import HttpUser, task, between
import json
import random
import time
from datetime import datetime, timedelta
import logging
from config import TestConfig

logger = logging.getLogger(__name__)

class TripSearchUser(HttpUser):
    """行程搜索性能测试用户"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """开始时登录"""
        self.login()
    
    def login(self):
        """用户登录"""
        user_data = random.choice(TestConfig.TEST_USERS)
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @task(5)
    def search_trips_basic(self):
        """基础行程搜索"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "page": 1,
            "size": 10
        }
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        trips = result.get("data", {}).get("records", [])
                        logger.info(f"搜索到 {len(trips)} 个行程")
                        response.success()
                    else:
                        response.failure(f"搜索失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("搜索响应JSON解析失败")
            else:
                response.failure(f"搜索请求失败: {response.status_code}")
    
    @task(3)
    def search_trips_with_time(self):
        """带时间的行程搜索"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        # 随机选择未来1-7天的日期
        future_date = datetime.now() + timedelta(days=random.randint(1, 7))
        departure_time = future_date.strftime("%Y-%m-%d")
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "departureTime": departure_time,
            "page": 1,
            "size": 10
        }
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"带时间搜索失败: {response.status_code}")
    
    @task(2)
    def search_trips_with_filters(self):
        """带过滤条件的行程搜索"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "minPrice": random.randint(10, 30),
            "maxPrice": random.randint(50, 100),
            "minSeats": random.randint(1, 2),
            "page": 1,
            "size": 20
        }
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"过滤搜索失败: {response.status_code}")
    
    @task(1)
    def search_trips_pagination(self):
        """分页搜索测试"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        page = random.randint(1, 5)
        size = random.choice([5, 10, 20, 50])
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "page": page,
            "size": size
        }
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"分页搜索失败: {response.status_code}")


class TripPublishUser(HttpUser):
    """行程发布性能测试用户"""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """开始时登录司机账户"""
        self.login_as_driver()
    
    def login_as_driver(self):
        """登录司机账户"""
        driver_users = [user for user in TestConfig.TEST_USERS if user["userType"] == "DRIVER"]
        user_data = random.choice(driver_users)
        
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @task(4)
    def publish_trip(self):
        """发布行程"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        # 随机选择未来1-7天的日期
        future_date = datetime.now() + timedelta(days=random.randint(1, 7))
        departure_time = future_date.strftime("%Y-%m-%d %H:%M")
        
        trip_data = {
            "startLocation": start_location,
            "endLocation": end_location,
            "departureTime": departure_time,
            "price": random.randint(20, 100),
            "seatAvailable": random.randint(1, 4),
            "description": f"从{start_location}到{end_location}的行程",
            "carId": random.randint(1, 10)
        }
        
        with self.client.post("/api/trips",
                            json=trip_data,
                            headers=self.get_headers(),
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        trip_id = result.get("data", {}).get("id")
                        logger.info(f"发布行程成功，ID: {trip_id}")
                        response.success()
                    else:
                        response.failure(f"发布行程失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("发布行程响应JSON解析失败")
            else:
                response.failure(f"发布行程请求失败: {response.status_code}")
    
    @task(2)
    def view_my_trips(self):
        """查看我的行程"""
        params = {
            "page": 1,
            "size": 10,
            "status": random.choice(["PUBLISHED", "CANCELLED", "COMPLETED", ""])
        }
        
        with self.client.get("/api/trips/my",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看我的行程失败: {response.status_code}")
    
    @task(1)
    def update_trip(self):
        """更新行程"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        
        update_data = {
            "price": random.randint(20, 100),
            "seatAvailable": random.randint(1, 4),
            "description": "更新后的行程描述"
        }
        
        with self.client.put(f"/api/trips/{trip_id}",
                           json=update_data,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"更新行程失败: {response.status_code}")
    
    @task(1)
    def cancel_trip(self):
        """取消行程"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        
        with self.client.put(f"/api/trips/{trip_id}/cancel",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"取消行程失败: {response.status_code}")


class TripDetailUser(HttpUser):
    """行程详情性能测试用户"""
    
    wait_time = between(1, 2)
    
    def on_start(self):
        """开始时登录"""
        self.login()
    
    def login(self):
        """用户登录"""
        user_data = random.choice(TestConfig.TEST_USERS)
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @task(5)
    def view_trip_detail(self):
        """查看行程详情"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        
        with self.client.get(f"/api/trips/{trip_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        trip_data = result.get("data", {})
                        logger.info(f"查看行程详情: {trip_data.get('startLocation')} -> {trip_data.get('endLocation')}")
                        response.success()
                    else:
                        response.failure(f"查看行程详情失败: {result.get('message')}")
                except json.JSONDecodeError:
                    response.failure("行程详情响应JSON解析失败")
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"查看行程详情请求失败: {response.status_code}")
    
    @task(2)
    def view_trip_bookings(self):
        """查看行程预订情况"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        
        with self.client.get(f"/api/trips/{trip_id}/bookings",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"查看行程预订失败: {response.status_code}")


class TripStressUser(HttpUser):
    """行程压力测试用户"""
    
    wait_time = between(0.1, 0.5)
    
    def on_start(self):
        """开始时登录"""
        self.login()
    
    def login(self):
        """用户登录"""
        user_data = random.choice(TestConfig.TEST_USERS)
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @task
    def rapid_search(self):
        """快速搜索"""
        start_location = random.choice(TestConfig.TEST_LOCATIONS)
        end_location = random.choice([loc for loc in TestConfig.TEST_LOCATIONS if loc != start_location])
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "page": 1,
            "size": 5
        }
        
        start_time = time.time()
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                if response_time > 2000:  # 超过2秒
                    logger.warning(f"搜索响应时间过长: {response_time:.2f}ms")
                response.success()
            else:
                response.failure(f"快速搜索失败: {response.status_code}")


class InvalidTripUser(HttpUser):
    """无效行程操作测试用户"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """开始时登录"""
        self.login()
    
    def login(self):
        """用户登录"""
        user_data = random.choice(TestConfig.TEST_USERS)
        response = self.client.post("/api/auth/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @task(3)
    def invalid_search(self):
        """无效搜索测试"""
        invalid_params_list = [
            {"startLocation": "", "endLocation": "上海"},
            {"startLocation": "北京", "endLocation": ""},
            {"startLocation": "不存在的地点", "endLocation": "上海"},
            {"page": -1, "size": 10},
            {"page": 1, "size": 0},
            {"page": 1, "size": 1000},  # 过大的size
        ]
        
        params = random.choice(invalid_params_list)
        
        with self.client.get("/api/trips/search",
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 400:
                # 预期的错误响应
                response.success()
            elif response.status_code == 200:
                # 某些情况下可能返回空结果
                response.success()
            else:
                response.failure(f"意外的响应状态码: {response.status_code}")
    
    @task(2)
    def invalid_publish(self):
        """无效发布测试"""
        invalid_data_list = [
            {"startLocation": "", "endLocation": "上海", "price": 50},
            {"startLocation": "北京", "endLocation": "", "price": 50},
            {"startLocation": "北京", "endLocation": "上海", "price": -10},
            {"startLocation": "北京", "endLocation": "上海", "price": 0},
            {"startLocation": "北京", "endLocation": "上海", "seatAvailable": 0},
            {"startLocation": "北京", "endLocation": "上海", "seatAvailable": -1},
        ]
        
        data = random.choice(invalid_data_list)
        
        with self.client.post("/api/trips",
                            json=data,
                            headers=self.get_headers(),
                            catch_response=True) as response:
            if response.status_code == 400:
                # 预期的错误响应
                response.success()
            elif response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") != 200:
                        # 业务逻辑错误
                        response.success()
                    else:
                        response.failure("无效数据不应该发布成功")
                except json.JSONDecodeError:
                    response.failure("发布响应JSON解析失败")
            else:
                response.failure(f"意外的响应状态码: {response.status_code}")
    
    @task(1)
    def access_nonexistent_trip(self):
        """访问不存在的行程"""
        trip_id = random.randint(99999, 999999)  # 很大的ID，应该不存在
        
        with self.client.get(f"/api/trips/{trip_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 404:
                # 预期的不存在响应
                response.success()
            else:
                response.failure(f"访问不存在行程应该返回404，实际: {response.status_code}") 