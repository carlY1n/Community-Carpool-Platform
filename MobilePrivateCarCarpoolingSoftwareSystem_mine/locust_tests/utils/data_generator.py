#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据生成工具
"""

import random
import time
from datetime import datetime, timedelta
from faker import Faker

# 创建中文Faker实例
fake = Faker('zh_CN')

class DataGenerator:
    """测试数据生成器"""
    
    # 中国城市列表
    CITIES = [
        "北京市", "上海市", "广州市", "深圳市", "杭州市", "南京市", "武汉市", "成都市",
        "重庆市", "天津市", "苏州市", "西安市", "长沙市", "沈阳市", "青岛市", "郑州市",
        "大连市", "东莞市", "宁波市", "厦门市", "福州市", "无锡市", "合肥市", "昆明市",
        "哈尔滨市", "济南市", "佛山市", "长春市", "温州市", "石家庄市", "南宁市", "常州市",
        "泉州市", "南昌市", "贵阳市", "太原市", "烟台市", "嘉兴市", "南通市", "金华市"
    ]
    
    # 上海具体地点
    SHANGHAI_LOCATIONS = [
        "上海市黄浦区人民广场", "上海市静安区静安寺", "上海市徐汇区徐家汇",
        "上海市浦东新区陆家嘴", "上海市长宁区中山公园", "上海市虹口区四川北路",
        "上海市杨浦区五角场", "上海市闵行区莘庄", "上海市宝山区大华",
        "上海市嘉定区嘉定北", "上海市松江区松江大学城", "上海市青浦区青浦新城",
        "上海市奉贤区南桥", "上海市金山区金山卫", "上海市崇明区堡镇"
    ]
    
    # 车辆品牌和型号
    CAR_BRANDS = [
        "大众", "丰田", "本田", "日产", "现代", "起亚", "福特", "雪佛兰",
        "别克", "奥迪", "宝马", "奔驰", "沃尔沃", "马自达", "斯巴鲁", "三菱"
    ]
    
    CAR_MODELS = [
        "朗逸", "轩逸", "卡罗拉", "速腾", "宝来", "捷达", "桑塔纳", "凯美瑞",
        "雅阁", "天籁", "帕萨特", "迈腾", "君威", "君越", "蒙迪欧", "福克斯"
    ]
    
    @staticmethod
    def generate_phone():
        """生成手机号"""
        prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '150', '151', '152', '153', '155', '156', '157', '158', '159',
                   '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + suffix
    
    @staticmethod
    def generate_id_card():
        """生成身份证号"""
        # 简化的身份证号生成（仅用于测试）
        area_codes = ['110101', '310101', '440101', '440301', '330101', '320101']
        area_code = random.choice(area_codes)
        birth_year = random.randint(1970, 2000)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = f"{birth_year}{birth_month:02d}{birth_day:02d}"
        sequence = random.randint(100, 999)
        check_digit = random.randint(0, 9)
        return f"{area_code}{birth_date}{sequence}{check_digit}"
    
    @staticmethod
    def generate_user_data(user_type="PASSENGER"):
        """生成用户数据"""
        timestamp = int(time.time())
        return {
            "username": fake.user_name() + str(timestamp % 1000),
            "phone": DataGenerator.generate_phone(),
            "password": "123456",
            "realName": fake.name(),
            "idCard": DataGenerator.generate_id_card(),
            "userType": user_type,
            "email": fake.email(),
            "avatar": fake.image_url()
        }
    
    @staticmethod
    def generate_trip_data():
        """生成行程数据"""
        start_location = random.choice(DataGenerator.CITIES)
        end_location = random.choice([city for city in DataGenerator.CITIES if city != start_location])
        
        # 生成未来1-30天的随机时间
        future_date = datetime.now() + timedelta(days=random.randint(1, 30))
        departure_time = future_date.strftime("%Y-%m-%d %H:%M")
        
        return {
            "startLocation": start_location,
            "endLocation": end_location,
            "departureTime": departure_time,
            "price": random.randint(20, 200),
            "seatAvailable": random.randint(1, 4),
            "description": f"从{start_location}到{end_location}的舒适行程",
            "carId": random.randint(1, 100),
            "driverRequirements": random.choice(["", "不吸烟", "安静", "可聊天", "准时"])
        }
    
    @staticmethod
    def generate_booking_data(trip_id=None):
        """生成预订数据"""
        if trip_id is None:
            trip_id = random.randint(1, 100)
        
        return {
            "tripId": trip_id,
            "passengerCount": random.randint(1, 3),
            "contactPhone": DataGenerator.generate_phone(),
            "remarks": random.choice([
                "准时到达", "有大件行李", "需要帮助搬运", "谢谢司机",
                "第一次使用", "请保持安静", "可以聊天", ""
            ])
        }
    
    @staticmethod
    def generate_car_data():
        """生成车辆数据"""
        brand = random.choice(DataGenerator.CAR_BRANDS)
        model = random.choice(DataGenerator.CAR_MODELS)
        
        # 生成车牌号（简化版）
        provinces = ['京', '沪', '粤', '浙', '苏', '鲁', '川', '湘', '豫', '冀']
        province = random.choice(provinces)
        letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
        digits = '0123456789'
        plate_number = f"{province}{random.choice(letters)}{random.choice(digits)}{random.choice(digits)}{random.choice(digits)}{random.choice(digits)}{random.choice(digits)}"
        
        return {
            "brand": brand,
            "model": model,
            "plateNumber": plate_number,
            "color": random.choice(["白色", "黑色", "银色", "红色", "蓝色", "灰色"]),
            "seatCount": random.choice([4, 5, 7]),
            "year": random.randint(2015, 2023)
        }
    
    @staticmethod
    def generate_complaint_data():
        """生成投诉数据"""
        complaint_types = [
            "司机迟到", "司机态度不好", "车辆不符", "路线不合理", 
            "乘客爽约", "乘客态度不好", "其他问题"
        ]
        
        return {
            "type": random.choice(complaint_types),
            "description": fake.text(max_nb_chars=200),
            "targetUserId": random.randint(1, 100),
            "tripId": random.randint(1, 100)
        }
    
    @staticmethod
    def generate_search_params():
        """生成搜索参数"""
        start_location = random.choice(DataGenerator.SHANGHAI_LOCATIONS)
        end_location = random.choice([loc for loc in DataGenerator.SHANGHAI_LOCATIONS if loc != start_location])
        
        params = {
            "startLocation": start_location,
            "endLocation": end_location,
            "page": random.randint(1, 5),
            "size": random.choice([5, 10, 20])
        }
        
        # 随机添加可选参数
        if random.random() < 0.3:  # 30%概率添加时间
            future_date = datetime.now() + timedelta(days=random.randint(1, 7))
            params["departureTime"] = future_date.strftime("%Y-%m-%d")
        
        if random.random() < 0.2:  # 20%概率添加价格范围
            min_price = random.randint(10, 30)
            max_price = min_price + random.randint(20, 50)
            params["minPrice"] = min_price
            params["maxPrice"] = max_price
        
        if random.random() < 0.1:  # 10%概率添加座位要求
            params["minSeats"] = random.randint(1, 2)
        
        return params
    
    @staticmethod
    def generate_invalid_data(data_type):
        """生成无效数据用于测试"""
        if data_type == "user":
            invalid_users = [
                {"phone": "123"},  # 无效手机号
                {"phone": "", "password": "123456"},  # 空手机号
                {"phone": "13800138000", "password": ""},  # 空密码
                {"phone": "13800138000", "password": "12"},  # 密码太短
                {},  # 空对象
            ]
            return random.choice(invalid_users)
        
        elif data_type == "trip":
            invalid_trips = [
                {"startLocation": "", "endLocation": "上海", "price": 50},  # 空起点
                {"startLocation": "北京", "endLocation": "", "price": 50},  # 空终点
                {"startLocation": "北京", "endLocation": "上海", "price": -10},  # 负价格
                {"startLocation": "北京", "endLocation": "上海", "seatAvailable": 0},  # 无座位
                {},  # 空对象
            ]
            return random.choice(invalid_trips)
        
        elif data_type == "booking":
            invalid_bookings = [
                {"tripId": -1, "passengerCount": 1},  # 无效行程ID
                {"tripId": 1, "passengerCount": 0},   # 无效乘客数
                {"tripId": 1, "passengerCount": -1},  # 负数乘客
                {},  # 空对象
            ]
            return random.choice(invalid_bookings)
        
        return {}
    
    @staticmethod
    def generate_batch_users(count, user_type="PASSENGER"):
        """批量生成用户数据"""
        users = []
        for i in range(count):
            user = DataGenerator.generate_user_data(user_type)
            # 确保手机号唯一
            user["phone"] = f"138{int(time.time()) + i:08d}"[-11:]
            users.append(user)
        return users
    
    @staticmethod
    def generate_batch_trips(count):
        """批量生成行程数据"""
        trips = []
        for _ in range(count):
            trip = DataGenerator.generate_trip_data()
            trips.append(trip)
        return trips
    
    @staticmethod
    def generate_performance_test_data():
        """生成性能测试专用数据"""
        return {
            "users": {
                "passengers": DataGenerator.generate_batch_users(50, "PASSENGER"),
                "drivers": DataGenerator.generate_batch_users(20, "DRIVER")
            },
            "trips": DataGenerator.generate_batch_trips(100),
            "locations": DataGenerator.SHANGHAI_LOCATIONS,
            "search_params": [DataGenerator.generate_search_params() for _ in range(20)]
        }


class TestDataManager:
    """测试数据管理器"""
    
    def __init__(self):
        self.users = []
        self.trips = []
        self.bookings = []
        self.cars = []
    
    def create_test_users(self, passenger_count=30, driver_count=10):
        """创建测试用户"""
        passengers = DataGenerator.generate_batch_users(passenger_count, "PASSENGER")
        drivers = DataGenerator.generate_batch_users(driver_count, "DRIVER")
        self.users = passengers + drivers
        return self.users
    
    def create_test_trips(self, count=50):
        """创建测试行程"""
        self.trips = DataGenerator.generate_batch_trips(count)
        return self.trips
    
    def get_random_user(self, user_type=None):
        """获取随机用户"""
        if user_type:
            filtered_users = [user for user in self.users if user["userType"] == user_type]
            return random.choice(filtered_users) if filtered_users else None
        return random.choice(self.users) if self.users else None
    
    def get_random_trip(self):
        """获取随机行程"""
        return random.choice(self.trips) if self.trips else None
    
    def cleanup_test_data(self):
        """清理测试数据"""
        self.users.clear()
        self.trips.clear()
        self.bookings.clear()
        self.cars.clear()


# 全局测试数据管理器实例
test_data_manager = TestDataManager()

if __name__ == "__main__":
    # 测试数据生成器
    print("=== 测试数据生成器 ===")
    
    # 生成用户数据
    user = DataGenerator.generate_user_data("PASSENGER")
    print(f"用户数据: {user}")
    
    # 生成行程数据
    trip = DataGenerator.generate_trip_data()
    print(f"行程数据: {trip}")
    
    # 生成预订数据
    booking = DataGenerator.generate_booking_data()
    print(f"预订数据: {booking}")
    
    # 生成搜索参数
    search_params = DataGenerator.generate_search_params()
    print(f"搜索参数: {search_params}")
    
    # 生成性能测试数据
    perf_data = DataGenerator.generate_performance_test_data()
    print(f"性能测试数据用户数: {len(perf_data['users']['passengers'])} 乘客, {len(perf_data['users']['drivers'])} 司机")
    print(f"性能测试数据行程数: {len(perf_data['trips'])}") 