#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼车系统性能测试 - Locust 测试文件
基于实际的后端 API 路径
"""

import json
import random
import logging
import hashlib
from datetime import datetime, timedelta
from locust import HttpUser, task, between, events

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 工具函数
def md5_encrypt(text):
    """MD5 加密"""
    return hashlib.md5(text.encode()).hexdigest()

# 登录请求类
class LoginRequest:
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password

class BaseUser(HttpUser):
    """基础用户类"""
    
    # 标记为抽象类，不会被 Locust 直接实例化
    abstract = True
    
    # 用户行为间隔时间（秒）
    wait_time = between(1, 3)
    
    # 测试数据 - 使用数据库中实际存在的用户（密码已 MD5 加密）
    test_users = [
        {"phone": "13800000001", "password": "e10adc3949ba59abbe56e057f20f883e", "userType": "DRIVER"},    # zhangsan (123456)
        {"phone": "13800000002", "password": "e10adc3949ba59abbe56e057f20f883e", "userType": "PASSENGER"}, # lisi (123456)
        {"phone": "13800000000", "password": "e10adc3949ba59abbe56e057f20f883e", "userType": "ADMIN"},     # admin (123456)
        # 添加更多测试用户（如果需要，可以先注册这些用户）
        {"phone": "13800138001", "password": "e10adc3949ba59abbe56e057f20f883e", "userType": "PASSENGER"},
        {"phone": "13800138002", "password": "e10adc3949ba59abbe56e057f20f883e", "userType": "DRIVER"},
    ]
    
    test_locations = [
        "北京市朝阳区", "北京市海淀区", "北京市西城区", "北京市东城区",
        "上海市浦东新区", "上海市黄浦区", "上海市徐汇区", "上海市静安区",
        "广州市天河区", "广州市越秀区", "深圳市南山区", "深圳市福田区"
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.user_info = None
    
    def on_start(self):
        """用户开始时执行登录"""
        self.login()
    
    def login(self):
        """用户登录"""
        user_data = random.choice(self.test_users)
        
        with self.client.post("/api/user/login", json={
            "phone": user_data["phone"],
            "password": user_data["password"]
        }, catch_response=True) as response:
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        # 根据实际返回结构调整
                        user_info = result.get("data")
                        if user_info:
                            self.user_info = user_info
                            # 假设返回的用户信息中包含 token 或 id
                            self.token = str(user_info.get("id", ""))
                        logger.info(f"用户登录成功: {user_data['phone']}")
                        response.success()
                    else:
                        logger.error(f"登录失败: {result.get('msg', result.get('message', '未知错误'))}")
                        response.failure(f"登录失败: {result.get('msg', result.get('message', '未知错误'))}")
                except json.JSONDecodeError:
                    response.failure("登录响应JSON解析失败")
            else:
                response.failure(f"登录请求失败: {response.status_code}")
    
    def get_headers(self):
        """获取请求头"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


class PassengerUser(BaseUser):
    """乘客用户行为模拟"""
    
    weight = 3  # 乘客用户权重（相对于司机用户更多）
    
    @task(5)
    def search_trips(self):
        """搜索行程"""
        # 使用经纬度搜索（根据实际 API）
        params = {
            "startLng": round(random.uniform(116.0, 117.0), 6),  # 北京经度范围
            "startLat": round(random.uniform(39.5, 40.5), 6),   # 北京纬度范围
            "endLng": round(random.uniform(116.0, 117.0), 6),
            "endLat": round(random.uniform(39.5, 40.5), 6),
            "departureTime": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d")
        }
        
        with self.client.get("/api/trip/search", 
                           params=params,
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                try:
                    trips = response.json()
                    if isinstance(trips, list):
                        logger.info(f"搜索到 {len(trips)} 个行程")
                        response.success()
                    else:
                        response.failure("搜索响应格式错误")
                except json.JSONDecodeError:
                    response.failure("搜索响应JSON解析失败")
            else:
                response.failure(f"搜索请求失败: {response.status_code}")
    
    @task(3)
    def view_trip_details(self):
        """查看行程详情"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        
        with self.client.get(f"/api/trip/{trip_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"查看行程详情失败: {response.status_code}")
    
    @task(2)
    def create_order(self):
        """创建订单"""
        trip_id = random.randint(1, 50)  # 假设的行程ID
        passenger_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        order_data = {
            "tripId": trip_id,
            "passengerId": passenger_id,
            "seatCount": random.randint(1, 3),
            "amount": random.randint(20, 100)
        }
        
        with self.client.post("/api/order/apply",
                            json=order_data,
                            headers=self.get_headers(),
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info("订单创建成功")
                    response.success()
                except json.JSONDecodeError:
                    response.failure("订单响应JSON解析失败")
            else:
                response.failure(f"创建订单请求失败: {response.status_code}")
    
    @task(2)
    def view_my_orders(self):
        """查看我的订单"""
        passenger_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        with self.client.get(f"/api/order/passenger/{passenger_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看订单失败: {response.status_code}")
    
    @task(1)
    def cancel_order(self):
        """取消订单"""
        order_id = random.randint(1, 100)  # 假设的订单ID
        
        with self.client.post(f"/api/order/cancel",
                           params={"orderId": order_id},
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 订单不存在也是正常情况
            else:
                response.failure(f"取消订单失败: {response.status_code}")


class DriverUser(BaseUser):
    """司机用户行为模拟"""
    
    weight = 1  # 司机用户权重
    
    @task(4)
    def publish_trip(self):
        """发布行程"""
        driver_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        trip_data = {
            "driverId": driver_id,
            "carId": random.randint(1, 10),
            "startLocation": random.choice(self.test_locations),
            "startLng": round(random.uniform(116.0, 117.0), 6),
            "startLat": round(random.uniform(39.5, 40.5), 6),
            "endLocation": random.choice(self.test_locations),
            "endLng": round(random.uniform(116.0, 117.0), 6),
            "endLat": round(random.uniform(39.5, 40.5), 6),
            "departureTime": (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat(),
            "price": random.randint(20, 100),
            "seatAvailable": random.randint(1, 4),
            "description": "测试行程"
        }
        
        with self.client.post("/api/trip/publish",
                            json=trip_data,
                            headers=self.get_headers(),
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info("发布行程成功")
                    response.success()
                except json.JSONDecodeError:
                    response.failure("发布行程响应JSON解析失败")
            else:
                response.failure(f"发布行程请求失败: {response.status_code}")
    
    @task(3)
    def view_my_trips(self):
        """查看我的行程"""
        driver_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        with self.client.get(f"/api/trip/driver/{driver_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看我的行程失败: {response.status_code}")
    
    @task(2)
    def manage_orders(self):
        """管理订单"""
        driver_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        with self.client.get(f"/api/order/driver/{driver_id}",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 没有订单也是正常情况
            else:
                response.failure(f"查看订单失败: {response.status_code}")
    
    @task(2)
    def confirm_order(self):
        """确认订单"""
        order_id = random.randint(1, 100)  # 假设的订单ID
        
        with self.client.post(f"/api/order/confirm",
                           params={"orderId": order_id},
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 订单不存在也是正常情况
            else:
                response.failure(f"确认订单失败: {response.status_code}")
    
    @task(1)
    def cancel_trip(self):
        """取消行程"""
        trip_id = random.randint(1, 100)  # 假设的行程ID
        driver_id = self.user_info.get("id") if self.user_info else random.randint(1, 100)
        
        with self.client.post(f"/api/trip/cancel/{trip_id}",
                           params={"driverId": driver_id},
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 行程不存在也是正常情况
            else:
                response.failure(f"取消行程失败: {response.status_code}")


class AdminUser(BaseUser):
    """管理员用户行为模拟"""
    
    weight = 0.1  # 管理员用户权重很低
    
    def on_start(self):
        """管理员登录"""
        self.token = None
        self.user_info = None
        self.admin_login()
    
    def admin_login(self):
        """管理员登录"""
        with self.client.post("/api/user/login", json={
            "phone": "13800000000",  # admin 用户的手机号
            "password": "e10adc3949ba59abbe56e057f20f883e"  # 123456 的 MD5
        }, catch_response=True) as response:
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        user_info = result.get("data")
                        if user_info:
                            self.user_info = user_info
                            self.token = str(user_info.get("id", ""))
                        logger.info("管理员登录成功")
                        response.success()
                    else:
                        response.failure(f"管理员登录失败: {result.get('msg', result.get('message', '未知错误'))}")
                except json.JSONDecodeError:
                    response.failure("管理员登录响应JSON解析失败")
            else:
                response.failure(f"管理员登录请求失败: {response.status_code}")
    
    @task(3)
    def view_all_users(self):
        """查看所有用户"""
        with self.client.get("/api/user/admin/list",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看用户列表失败: {response.status_code}")
    
    @task(2)
    def view_all_trips(self):
        """查看所有行程"""
        with self.client.get("/api/trip/admin/list",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看行程列表失败: {response.status_code}")
    
    @task(2)
    def view_pending_cars(self):
        """查看待审核车辆"""
        with self.client.get("/api/car/pending",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看待审核车辆失败: {response.status_code}")
    
    @task(1)
    def view_complaints(self):
        """查看投诉"""
        with self.client.get("/api/complaint/pending",
                           headers=self.get_headers(),
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"查看投诉列表失败: {response.status_code}")


# 事件监听器
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始时执行"""
    logger.info("=== 拼车系统性能测试开始 ===")
    logger.info(f"目标主机: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束时执行"""
    logger.info("=== 拼车系统性能测试结束 ===")


# 如果直接运行此文件，使用默认配置
if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://localhost:8888") 