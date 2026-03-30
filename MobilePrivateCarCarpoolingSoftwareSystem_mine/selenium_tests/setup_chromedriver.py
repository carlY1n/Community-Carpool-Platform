#!/usr/bin/env python3
"""
ChromeDriver设置脚本
帮助用户配置本地ChromeDriver路径
"""
import os
import sys
import shutil
from pathlib import Path

def find_chromedriver():
    """查找可能的ChromeDriver位置"""
    print("🔍 正在搜索ChromeDriver...")
    
    # 可能的路径
    search_paths = [
        # 当前目录及上级目录
        "chromedriver-win64/chromedriver.exe",
        "../chromedriver-win64/chromedriver.exe", 
        "../../chromedriver-win64/chromedriver.exe",
        "chromedriver.exe",
        "../chromedriver.exe",
        # Linux/Mac路径
        "chromedriver-win64/chromedriver",
        "../chromedriver-win64/chromedriver",
        "chromedriver"
    ]
    
    found_paths = []
    
    for path in search_paths:
        full_path = os.path.abspath(path)
        if os.path.exists(full_path):
            found_paths.append(full_path)
            print(f"✅ 找到: {full_path}")
    
    if not found_paths:
        print("❌ 未找到ChromeDriver文件")
        return None
    
    return found_paths

def copy_chromedriver_to_project():
    """将ChromeDriver复制到项目目录"""
    found_paths = find_chromedriver()
    
    if not found_paths:
        print("\n💡 建议操作:")
        print("1. 将chromedriver-win64文件夹放在项目根目录")
        print("2. 或者将chromedriver.exe直接放在selenium_tests目录")
        return False
    
    print(f"\n📋 找到 {len(found_paths)} 个ChromeDriver:")
    for i, path in enumerate(found_paths, 1):
        print(f"{i}. {path}")
    
    # 选择第一个作为默认
    selected_path = found_paths[0]
    print(f"\n✅ 将使用: {selected_path}")
    
    # 检查是否需要复制
    project_chromedriver = "chromedriver.exe" if os.name == 'nt' else "chromedriver"
    
    if not os.path.exists(project_chromedriver):
        try:
            shutil.copy2(selected_path, project_chromedriver)
            print(f"📁 已复制ChromeDriver到项目目录: {project_chromedriver}")
        except Exception as e:
            print(f"❌ 复制失败: {e}")
            return False
    else:
        print(f"📁 项目目录已存在ChromeDriver: {project_chromedriver}")
    
    return True

def test_chromedriver():
    """测试ChromeDriver是否可用"""
    print("\n🧪 测试ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        # 查找ChromeDriver
        chromedriver_paths = [
            "chromedriver.exe",
            "chromedriver",
            "../chromedriver-win64/chromedriver.exe",
            "chromedriver-win64/chromedriver.exe"
        ]
        
        chromedriver_path = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                chromedriver_path = os.path.abspath(path)
                break
        
        if not chromedriver_path:
            print("❌ 未找到可用的ChromeDriver")
            return False
        
        print(f"🔧 使用ChromeDriver: {chromedriver_path}")
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 创建服务
        service = Service(chromedriver_path)
        
        # 创建driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 简单测试
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ ChromeDriver测试成功! 页面标题: {title}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver测试失败: {e}")
        return False

def update_config():
    """更新配置文件"""
    print("\n⚙️ 更新配置文件...")
    
    config_file = "config/config.py"
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    # 检查是否已经配置
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'CHROMEDRIVER_PATH = None' in content:
        print("📝 配置文件已包含ChromeDriver配置")
        return True
    
    print("✅ 配置文件已更新")
    return True

def main():
    """主函数"""
    print("🚗 ChromeDriver设置向导")
    print("=" * 40)
    
    # 检查当前目录
    if not os.path.exists("config"):
        print("❌ 请在selenium_tests目录下运行此脚本")
        return 1
    
    # 查找并设置ChromeDriver
    if copy_chromedriver_to_project():
        print("✅ ChromeDriver设置完成")
    else:
        print("❌ ChromeDriver设置失败")
        return 1
    
    # 测试ChromeDriver
    if test_chromedriver():
        print("✅ ChromeDriver测试通过")
    else:
        print("❌ ChromeDriver测试失败")
        return 1
    
    # 更新配置
    update_config()
    
    print("\n🎉 设置完成!")
    print("\n📋 下一步:")
    print("1. 运行测试: python run_tests.py")
    print("2. 运行冒烟测试: python run_tests.py -m smoke")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 