#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Locust性能测试配置文件
"""

import os
from datetime import datetime

class TestConfig:
    """测试配置类"""
    
    # 服务器配置
    HOST = os.getenv("TEST_HOST", "http://localhost:8888")
    
    # 备用服务器地址
    BACKUP_HOSTS = [
        "http://localhost:8080",
        "http://localhost:9090", 
        "http://localhost:8000"
    ]
    
    # 用户配置
    USERS = int(os.getenv("USERS", "50"))  # 并发用户数
    SPAWN_RATE = float(os.getenv("SPAWN_RATE", "2"))  # 每秒启动用户数
    RUN_TIME = os.getenv("RUN_TIME", "5m")  # 运行时间
    
    # 测试数据配置
    TEST_USERS = [
        {"phone": "13800138001", "password": "123456", "userType": "PASSENGER"},
        {"phone": "13800138002", "password": "123456", "userType": "DRIVER"},
        {"phone": "13800138003", "password": "123456", "userType": "PASSENGER"},
        {"phone": "13800138004", "password": "123456", "userType": "DRIVER"},
        {"phone": "13800138005", "password": "123456", "userType": "PASSENGER"},
        {"phone": "13800138006", "password": "123456", "userType": "DRIVER"},
        {"phone": "13800138007", "password": "123456", "userType": "PASSENGER"},
        {"phone": "13800138008", "password": "123456", "userType": "DRIVER"},
        {"phone": "13800138009", "password": "123456", "userType": "PASSENGER"},
        {"phone": "13800138010", "password": "123456", "userType": "DRIVER"},
    ]
    
    # 管理员账户
    ADMIN_USER = {
        "username": "admin",
        "password": "admin123"
    }
    
    # 测试地点
    TEST_LOCATIONS = [
        "上海市黄浦区人民广场",
        "上海市静安区静安寺",
        "上海市徐汇区徐家汇",
        "上海市浦东新区陆家嘴",
        "上海市长宁区中山公园",
        "上海市虹口区四川北路",
        "上海市杨浦区五角场",
        "上海市闵行区莘庄",
        "上海市宝山区大华",
        "上海市嘉定区嘉定北",
        "上海市松江区松江大学城",
        "上海市青浦区青浦新城",
        "上海市奉贤区南桥",
        "上海市金山区金山卫",
        "上海市崇明区堡镇"
    ]
    
    # API端点配置
    API_ENDPOINTS = {
        "auth": {
            "login": "/api/auth/login",
            "register": "/api/auth/register",
            "logout": "/api/auth/logout",
            "refresh": "/api/auth/refresh"
        },
        "user": {
            "profile": "/api/user/profile",
            "update": "/api/user/update",
            "cars": "/api/user/cars"
        },
        "trip": {
            "search": "/api/trips/search",
            "publish": "/api/trips",
            "detail": "/api/trips/{id}",
            "my_trips": "/api/trips/my",
            "cancel": "/api/trips/{id}/cancel",
            "bookings": "/api/trips/{id}/bookings"
        },
        "booking": {
            "create": "/api/bookings",
            "my_bookings": "/api/bookings/my",
            "detail": "/api/bookings/{id}",
            "confirm": "/api/bookings/{id}/confirm",
            "cancel": "/api/bookings/{id}/cancel"
        },
        "admin": {
            "users": "/api/admin/users",
            "trips": "/api/admin/trips",
            "bookings": "/api/admin/bookings",
            "complaints": "/api/admin/complaints",
            "statistics": "/api/admin/statistics"
        }
    }
    
    # 性能测试阈值
    PERFORMANCE_THRESHOLDS = {
        "response_time_95": 2000,  # 95%响应时间阈值(ms)
        "response_time_avg": 500,  # 平均响应时间阈值(ms)
        "error_rate": 0.05,  # 错误率阈值(5%)
        "rps_min": 10  # 最小RPS
    }
    
    # 报告配置
    REPORT_CONFIG = {
        "html_report": True,
        "csv_report": True,
        "report_dir": f"reports/{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": "拼车系统性能测试报告"
    }
    
    # 日志配置
    LOG_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": f"logs/locust_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    }


class ScenarioConfig:
    """测试场景配置"""
    
    # 轻负载测试
    LIGHT_LOAD = {
        "users": 10,
        "spawn_rate": 1,
        "run_time": "2m",
        "description": "轻负载测试 - 验证基本功能"
    }
    
    # 正常负载测试
    NORMAL_LOAD = {
        "users": 50,
        "spawn_rate": 2,
        "run_time": "5m",
        "description": "正常负载测试 - 模拟日常使用"
    }
    
    # 高负载测试
    HIGH_LOAD = {
        "users": 100,
        "spawn_rate": 5,
        "run_time": "10m",
        "description": "高负载测试 - 模拟高峰期使用"
    }
    
    # 压力测试
    STRESS_TEST = {
        "users": 200,
        "spawn_rate": 10,
        "run_time": "15m",
        "description": "压力测试 - 测试系统极限"
    }
    
    # 峰值测试
    SPIKE_TEST = {
        "users": 500,
        "spawn_rate": 50,
        "run_time": "3m",
        "description": "峰值测试 - 测试突发流量"
    }
    
    # 稳定性测试
    STABILITY_TEST = {
        "users": 30,
        "spawn_rate": 1,
        "run_time": "30m",
        "description": "稳定性测试 - 长时间运行"
    }


# 环境变量配置
def get_config_from_env():
    """从环境变量获取配置"""
    return {
        "host": os.getenv("LOCUST_HOST", TestConfig.HOST),
        "users": int(os.getenv("LOCUST_USERS", TestConfig.USERS)),
        "spawn_rate": float(os.getenv("LOCUST_SPAWN_RATE", TestConfig.SPAWN_RATE)),
        "run_time": os.getenv("LOCUST_RUN_TIME", TestConfig.RUN_TIME),
        "headless": os.getenv("LOCUST_HEADLESS", "false").lower() == "true",
        "csv": os.getenv("LOCUST_CSV", ""),
        "html": os.getenv("LOCUST_HTML", "")
    } 