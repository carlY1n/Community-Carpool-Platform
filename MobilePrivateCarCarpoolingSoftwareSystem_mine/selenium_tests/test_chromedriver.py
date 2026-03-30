#!/usr/bin/env python3
"""
ChromeDriver快速测试脚本
验证ChromeDriver配置是否正确
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_manager import DriverManager
from config.config import TestConfig

def test_chromedriver_basic():
    """基础ChromeDriver测试"""
    print("🧪 开始ChromeDriver基础测试...")
    
    try:
        # 创建driver管理器
        dm = DriverManager()
        
        # 创建driver（无头模式）
        driver = dm.create_driver(headless=True, mobile_emulation=False)
        
        print("✅ ChromeDriver创建成功")
        
        # 访问测试页面
        driver.get("https://www.google.com")
        title = driver.title
        print(f"✅ 页面访问成功，标题: {title}")
        
        # 清理
        dm.quit_driver()
        print("✅ ChromeDriver测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver测试失败: {e}")
        return False

def test_mobile_emulation():
    """移动端模拟测试"""
    print("\n📱 开始移动端模拟测试...")
    
    try:
        # 创建driver管理器
        dm = DriverManager()
        
        # 创建driver（移动端模拟）
        driver = dm.create_driver(headless=True, mobile_emulation=True)
        
        print("✅ 移动端模拟ChromeDriver创建成功")
        
        # 检查窗口大小
        size = driver.get_window_size()
        print(f"✅ 窗口大小: {size['width']}x{size['height']}")
        
        # 检查User-Agent
        user_agent = driver.execute_script("return navigator.userAgent;")
        if "iPhone" in user_agent:
            print("✅ User-Agent包含iPhone标识")
        else:
            print(f"⚠️ User-Agent: {user_agent}")
        
        # 清理
        dm.quit_driver()
        print("✅ 移动端模拟测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 移动端模拟测试失败: {e}")
        return False

def test_local_app():
    """测试本地应用访问"""
    print("\n🌐 开始本地应用访问测试...")
    
    try:
        # 创建driver管理器
        dm = DriverManager()
        
        # 创建driver
        driver = dm.create_driver(headless=True, mobile_emulation=True)
        
        # 访问本地前端
        frontend_url = TestConfig.BASE_URL
        print(f"🔗 访问前端: {frontend_url}")
        
        driver.get(frontend_url)
        dm.wait_for_page_load()
        
        title = driver.title
        current_url = driver.current_url
        
        print(f"✅ 前端访问成功")
        print(f"   标题: {title}")
        print(f"   URL: {current_url}")
        
        # 清理
        dm.quit_driver()
        print("✅ 本地应用访问测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 本地应用访问测试失败: {e}")
        print("💡 请确保前端应用运行在 http://localhost:8080")
        return False

def main():
    """主函数"""
    print("🚗 ChromeDriver配置测试")
    print("=" * 40)
    
    success_count = 0
    total_tests = 3
    
    # 基础测试
    if test_chromedriver_basic():
        success_count += 1
    
    # 移动端模拟测试
    if test_mobile_emulation():
        success_count += 1
    
    # 本地应用测试
    if test_local_app():
        success_count += 1
    
    print(f"\n📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！ChromeDriver配置正确")
        print("\n📋 下一步:")
        print("1. 运行完整测试: python run_tests.py")
        print("2. 运行冒烟测试: python run_tests.py -m smoke")
        return 0
    else:
        print("❌ 部分测试失败，请检查配置")
        print("\n💡 故障排除:")
        print("1. 确保Chrome浏览器已安装")
        print("2. 检查ChromeDriver版本是否与Chrome匹配")
        print("3. 运行: python setup_chromedriver.py")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 