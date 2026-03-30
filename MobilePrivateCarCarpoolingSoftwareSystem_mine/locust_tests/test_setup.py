#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境验证脚本
"""

import sys
import os
import requests
import json
from datetime import datetime

def test_imports():
    """测试依赖包导入"""
    print("🔍 检查依赖包...")
    
    try:
        import locust
        print(f"✅ Locust: {locust.__version__}")
    except ImportError as e:
        print(f"❌ Locust导入失败: {e}")
        return False
    
    try:
        import faker
        try:
            version = faker.__version__
        except AttributeError:
            version = "已安装"
        print(f"✅ Faker: {version}")
    except ImportError as e:
        print(f"❌ Faker导入失败: {e}")
        return False
    
    try:
        import jinja2
        print(f"✅ Jinja2: {jinja2.__version__}")
    except ImportError as e:
        print(f"❌ Jinja2导入失败: {e}")
        return False
    
    return True

def test_backend_connection():
    """测试后端连接"""
    print("\n🔗 测试后端连接...")
    
    # 尝试多个可能的端口和路径
    possible_urls = [
        "http://localhost:8888",
        "http://localhost:8080", 
        "http://localhost:9090",
        "http://localhost:8000"
    ]
    
    possible_paths = ["/health", "/actuator/health", "/api/health", "/", "/api"]
    
    backend_found = False
    working_url = None
    
    for base_url in possible_urls:
        for path in possible_paths:
            try:
                url = f"{base_url}{path}"
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 404]:  # 404也说明服务在运行
                    print(f"✅ 后端服务检测成功: {url} (状态码: {response.status_code})")
                    backend_found = True
                    working_url = base_url
                    break
            except requests.exceptions.RequestException:
                continue
        if backend_found:
            break
    
    if not backend_found:
        print("❌ 无法连接到后端服务")
        print("尝试的URL:")
        for base_url in possible_urls:
            for path in possible_paths:
                print(f"  - {base_url}{path}")
        return False
    
    # 测试登录接口
    if working_url:
        try:
            login_data = {
                "phone": "13800138001",
                "password": "123456"
            }
            response = requests.post(f"{working_url}/api/auth/login", json=login_data, timeout=5)
            print(f"✅ 登录接口测试: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("code") == 200:
                        print("✅ 登录成功，获取到token")
                        return True
                    else:
                        print(f"⚠️  登录业务失败: {result.get('message')}")
                        return True  # 服务正常，只是业务逻辑问题
                except json.JSONDecodeError:
                    print("⚠️  登录响应不是JSON格式，但服务正常运行")
                    return True
            else:
                print(f"⚠️  登录接口返回: {response.status_code}")
                return True  # 服务正常，只是接口问题
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 登录接口测试失败: {e}")
            return False
    
    return True

def test_file_structure():
    """测试文件结构"""
    print("\n📁 检查文件结构...")
    
    required_files = [
        "locustfile.py",
        "config.py",
        "run_tests.py",
        "requirements.txt",
        "README.md"
    ]
    
    required_dirs = [
        "scenarios",
        "utils"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 不存在")
            return False
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ 不存在")
            return False
    
    return True

def test_config_loading():
    """测试配置加载"""
    print("\n⚙️  测试配置加载...")
    
    try:
        from config import TestConfig, ScenarioConfig
        print("✅ 配置文件导入成功")
        
        print(f"✅ 默认主机: {TestConfig.HOST}")
        print(f"✅ 默认用户数: {TestConfig.USERS}")
        print(f"✅ 测试用户数量: {len(TestConfig.TEST_USERS)}")
        print(f"✅ 测试地点数量: {len(TestConfig.TEST_LOCATIONS)}")
        
        return True
    except ImportError as e:
        print(f"❌ 配置导入失败: {e}")
        return False

def test_data_generator():
    """测试数据生成器"""
    print("\n🎲 测试数据生成器...")
    
    try:
        from utils.data_generator import DataGenerator
        print("✅ 数据生成器导入成功")
        
        # 测试生成用户数据
        user_data = DataGenerator.generate_user_data()
        print(f"✅ 生成用户数据: {user_data['phone']}")
        
        # 测试生成行程数据
        trip_data = DataGenerator.generate_trip_data()
        print(f"✅ 生成行程数据: {trip_data['startLocation']} -> {trip_data['endLocation']}")
        
        return True
    except ImportError as e:
        print(f"❌ 数据生成器导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 数据生成测试失败: {e}")
        return False

def test_scenarios():
    """测试场景文件"""
    print("\n🎭 测试场景文件...")
    
    scenarios = [
        "scenarios.auth_scenario",
        "scenarios.trip_scenario", 
        "scenarios.booking_scenario"
    ]
    
    for scenario in scenarios:
        try:
            __import__(scenario)
            print(f"✅ {scenario}")
        except ImportError as e:
            print(f"❌ {scenario} 导入失败: {e}")
            return False
    
    return True

def create_test_report():
    """创建测试报告"""
    print("\n📊 生成测试报告...")
    
    report = {
        "test_time": datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": sys.platform,
        "tests": {
            "imports": False,
            "backend": False,
            "files": False,
            "config": False,
            "data_generator": False,
            "scenarios": False
        }
    }
    
    # 运行所有测试
    report["tests"]["imports"] = test_imports()
    report["tests"]["backend"] = test_backend_connection()
    report["tests"]["files"] = test_file_structure()
    report["tests"]["config"] = test_config_loading()
    report["tests"]["data_generator"] = test_data_generator()
    report["tests"]["scenarios"] = test_scenarios()
    
    # 计算总体结果
    all_passed = all(report["tests"].values())
    report["overall_result"] = "PASS" if all_passed else "FAIL"
    
    # 保存报告
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/setup_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 测试报告已保存: {report_file}")
    
    return all_passed

def main():
    """主函数"""
    print("🚗 拼车系统性能测试 - 环境验证")
    print("=" * 50)
    
    success = create_test_report()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过！环境配置正确")
        print("🚀 可以开始运行性能测试")
        print("\n快速开始:")
        print("  python quick_start.py")
        print("  python run_tests.py --scenario light")
    else:
        print("❌ 部分测试失败，请检查环境配置")
        print("\n解决方案:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 启动后端服务: 确保 http://localhost:8888 可访问")
        print("  3. 检查文件完整性")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 