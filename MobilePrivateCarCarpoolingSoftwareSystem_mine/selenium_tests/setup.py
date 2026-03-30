#!/usr/bin/env python3
"""
拼车系统Selenium测试项目设置脚本
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def check_chrome():
    """检查Chrome浏览器"""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ 找到Chrome浏览器: {path}")
            return True
    
    print("❌ 未找到Chrome浏览器，请先安装Chrome")
    return False

def setup_chromedriver():
    """设置ChromeDriver"""
    print("🔧 设置ChromeDriver...")
    
    # 查找本地ChromeDriver
    chromedriver_paths = [
        "../chromedriver-win64/chromedriver.exe",
        "chromedriver-win64/chromedriver.exe",
        "./chromedriver-win64/chromedriver.exe",
        "chromedriver.exe",
        "../chromedriver-win64/chromedriver",
        "chromedriver-win64/chromedriver",
        "chromedriver"
    ]
    
    found_path = None
    for path in chromedriver_paths:
        if os.path.exists(path):
            found_path = os.path.abspath(path)
            print(f"✅ 找到本地ChromeDriver: {found_path}")
            break
    
    if found_path:
        print("✅ 将使用本地ChromeDriver")
        return True
    else:
        print("⚠️ 未找到本地ChromeDriver，将使用自动下载")
        print("💡 如果您有chromedriver-win64文件夹，请将其放在项目根目录")
        return True

def install_dependencies():
    """安装项目依赖"""
    print("📦 正在安装项目依赖...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("✅ 依赖安装成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_directories():
    """创建必要的目录"""
    dirs = ["screenshots", "reports", "logs"]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"📁 创建目录: {dir_name}")

def check_services():
    """检查前后端服务状态"""
    import requests
    
    services = [
        ("前端服务", "http://localhost:8080"),
        ("后端API", "http://localhost:8888/api/user/types")
    ]
    
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 400:
                print(f"✅ {name}运行正常: {url}")
            else:
                print(f"⚠️ {name}响应异常: {url} (状态码: {response.status_code})")
        except requests.exceptions.RequestException:
            print(f"❌ {name}无法访问: {url}")

def run_demo_test():
    """运行演示测试"""
    print("\n🧪 运行演示测试...")
    
    try:
        result = subprocess.run([
            sys.executable, "run_tests.py", 
            "-m", "smoke", 
            "-v",
            "--html-report"
        ], check=False)
        
        if result.returncode == 0:
            print("✅ 演示测试运行成功")
        else:
            print("⚠️ 演示测试运行完成，请查看详细日志")
            
    except Exception as e:
        print(f"❌ 运行演示测试失败: {e}")

def main():
    """主函数"""
    print("🚗 拼车系统Selenium功能测试项目设置")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return 1
    
    # 检查Chrome浏览器
    if not check_chrome():
        return 1
    
    # 设置ChromeDriver
    setup_chromedriver()
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    if not install_dependencies():
        return 1
    
    print("\n🔍 检查服务状态...")
    check_services()
    
    print("\n✅ 项目设置完成！")
    print("\n📋 下一步操作：")
    print("1. 确保前端应用运行在 http://localhost:8080")
    print("2. 确保后端API运行在 http://localhost:8888")
    print("3. 运行测试：")
    print("   python run_tests.py                    # 运行所有测试")
    print("   python run_tests.py -m smoke          # 运行冒烟测试")
    print("   python run_tests.py --html-report     # 生成HTML报告")
    print("   python run_tests.py --headless        # 无头模式运行")
    
    # 询问是否运行演示测试
    if input("\n是否运行演示测试? (y/N): ").lower() in ['y', 'yes']:
        run_demo_test()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 