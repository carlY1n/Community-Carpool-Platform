"""
测试配置文件
"""
import os
from typing import Dict, Any

class TestConfig:
    """测试配置类"""
    
    # 基础配置
    BASE_URL = "http://localhost:8080"
    API_BASE_URL = "http://localhost:8888"
    
    # ChromeDriver配置
    CHROMEDRIVER_PATH = None  # 如果设置了路径，将优先使用；否则自动下载
    
    # Chrome浏览器配置
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",  # 可选：禁用图片加载以提高速度
    ]
    
    # 测试用户数据
    TEST_USERS = {
        "passenger": {
            "username": "test_passenger",
            "password": "123456",
            "phone": "13800138001",
            "realName": "测试乘客",
            "idCard": "310101199001011234",
            "userType": "PASSENGER"
        },
        "driver": {
            "username": "test_driver", 
            "password": "123456",
            "phone": "13800138002",
            "realName": "测试司机",
            "idCard": "310101199001011235",
            "userType": "DRIVER"
        },
        "admin": {
            "username": "admin",
            "password": "admin123",
            "phone": "13800138000",
            "realName": "管理员",
            "idCard": "310101199001011236",
            "userType": "ADMIN"
        }
    }
    
    # 测试数据
    TEST_TRIP_DATA = {
        "startLocation": "上海市黄浦区人民广场",
        "endLocation": "上海市静安区静安寺", 
        "departureTime": "2024-12-25 09:00",
        "price": "25",
        "seatAvailable": "3",
        "description": "舒适出行，准时到达"
    }
    
    # 页面元素等待时间
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    
    # 截图配置
    SCREENSHOT_DIR = "screenshots"
    REPORT_DIR = "reports"
    
    # 测试环境检查URL
    HEALTH_CHECK_URLS = [
        f"{BASE_URL}",
        f"{API_BASE_URL}/api/user/types"
    ]
    
    @classmethod
    def get_chromedriver_paths(cls):
        """
        获取可能的ChromeDriver路径列表
        
        Returns:
            list: ChromeDriver路径列表
        """
        return [
            # 用户指定的路径
            cls.CHROMEDRIVER_PATH,
            # 项目根目录下的chromedriver-win64文件夹
            "../chromedriver-win64/chromedriver.exe",
            "chromedriver-win64/chromedriver.exe", 
            "./chromedriver-win64/chromedriver.exe",
            "../../chromedriver-win64/chromedriver.exe",
            # 当前目录
            "chromedriver.exe",
            "./chromedriver.exe",
            # Linux/Mac路径
            "../chromedriver-win64/chromedriver",
            "chromedriver-win64/chromedriver",
            "./chromedriver-win64/chromedriver",
            "chromedriver"
        ]

class PageConfig:
    """页面配置类"""
    
    # 页面路径
    PAGES = {
        "login": "/pages/login/login",
        "register": "/pages/register/register", 
        "index": "/pages/index/index",
        "search_trip": "/pages/searchTrip/searchTrip",
        "publish_trip": "/pages/publishTrip/publishTrip",
        "my_orders": "/pages/myOrders/myOrders",
        "my_trips": "/pages/myTrips/myTrips",
        "profile": "/pages/profile/profile",
        "car_manage": "/pages/carManage/carManage",
        "complaints": "/pages/complaints/complaints",
        "admin_user": "/pages/admin/user",
        "admin_trip": "/pages/admin/trip",
        "admin_complaint": "/pages/admin/complaint"
    }
    
    # 常用元素选择器
    COMMON_SELECTORS = {
        "loading": ".uni-loading",
        "toast": ".uni-toast",
        "modal": ".uni-modal",
        "back_button": ".uni-page-head-btn",
        "tab_bar": ".uni-tabbar"
    } 