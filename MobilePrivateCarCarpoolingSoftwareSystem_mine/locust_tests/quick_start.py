#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼车系统性能测试 - 快速启动脚本
"""

import os
import sys
import subprocess
import time
import requests
from datetime import datetime

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要Python 3.7或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def check_backend_service():
    """检查后端服务是否运行"""
    # 尝试多个可能的端口和路径
    possible_urls = [
        "http://localhost:8888",
        "http://localhost:8080", 
        "http://localhost:9090",
        "http://localhost:8000"
    ]
    
    possible_paths = ["/health", "/actuator/health", "/api/health", "/", "/api"]
    
    for base_url in possible_urls:
        for path in possible_paths:
            try:
                url = f"{base_url}{path}"
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 404]:  # 404也说明服务在运行
                    print(f"✅ 后端服务运行正常: {base_url}")
                    return True
            except:
                continue
    
    print("⚠️  后端服务未运行或无法访问")
    print("   尝试的地址: http://localhost:8888, :8080, :9090, :8000")
    print("   请确保拼车系统后端服务已启动")
    return False

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败")
        return False

def create_directories():
    """创建必要的目录"""
    directories = ["reports", "logs"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 创建目录: {directory}")

def run_quick_test():
    """运行快速测试"""
    print("\n🚀 开始快速性能测试...")
    print("=" * 50)
    
    cmd = [
        sys.executable, "run_tests.py",
        "--scenario", "light",
        "--users", "5",
        "--spawn-rate", "1",
        "--run-time", "1m"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 快速测试完成!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ 快速测试失败")
        return False

def show_menu():
    """显示菜单"""
    print("\n" + "=" * 60)
    print("🚗 拼车系统性能测试 - 快速启动")
    print("=" * 60)
    print("1. 快速测试 (5用户, 1分钟)")
    print("2. 正常测试 (50用户, 5分钟)")
    print("3. 启动Web UI")
    print("4. 认证模块测试")
    print("5. 行程模块测试")
    print("6. 预订模块测试")
    print("7. 查看测试报告")
    print("8. 系统检查")
    print("0. 退出")
    print("=" * 60)

def run_normal_test():
    """运行正常测试"""
    print("\n🚀 开始正常负载测试...")
    cmd = [sys.executable, "run_tests.py", "--scenario", "normal"]
    subprocess.run(cmd)

def start_web_ui():
    """启动Web UI"""
    print("\n🌐 启动Locust Web UI...")
    print("🔗 访问地址: http://localhost:8089")
    cmd = [sys.executable, "run_tests.py", "--web-ui"]
    subprocess.run(cmd)

def run_module_test(module):
    """运行模块测试"""
    print(f"\n🧪 开始{module}模块测试...")
    cmd = [sys.executable, "run_tests.py", f"--{module}-only"]
    subprocess.run(cmd)

def view_reports():
    """查看测试报告"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        print("❌ 报告目录不存在")
        return
    
    files = os.listdir(reports_dir)
    html_files = [f for f in files if f.endswith('.html')]
    
    if not html_files:
        print("❌ 没有找到HTML报告文件")
        return
    
    print(f"\n📋 找到 {len(html_files)} 个报告文件:")
    for i, file in enumerate(html_files, 1):
        file_path = os.path.join(reports_dir, file)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"{i}. {file} ({file_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    try:
        choice = int(input("\n选择要查看的报告 (输入序号): "))
        if 1 <= choice <= len(html_files):
            file_path = os.path.join(reports_dir, html_files[choice-1])
            abs_path = os.path.abspath(file_path)
            print(f"📖 报告路径: {abs_path}")
            
            # 尝试在浏览器中打开
            try:
                import webbrowser
                webbrowser.open(f"file://{abs_path}")
                print("✅ 已在浏览器中打开报告")
            except:
                print("⚠️  无法自动打开浏览器，请手动打开上述路径")
        else:
            print("❌ 无效的选择")
    except ValueError:
        print("❌ 请输入有效的数字")

def system_check():
    """系统检查"""
    print("\n🔍 系统检查...")
    print("=" * 40)
    
    # 检查Python版本
    check_python_version()
    
    # 检查依赖包
    try:
        import locust
        print(f"✅ Locust版本: {locust.__version__}")
    except ImportError:
        print("❌ Locust未安装")
    
    try:
        import requests
        print(f"✅ Requests版本: {requests.__version__}")
    except ImportError:
        print("❌ Requests未安装")
    
    # 检查后端服务
    check_backend_service()
    
    # 检查目录
    directories = ["reports", "logs"]
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ 目录存在: {directory}")
        else:
            print(f"⚠️  目录不存在: {directory}")
    
    print("=" * 40)

def main():
    """主函数"""
    # 初始化
    create_directories()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (0-8): ").strip()
            
            if choice == "0":
                print("👋 再见!")
                break
            elif choice == "1":
                if not check_backend_service():
                    continue
                run_quick_test()
            elif choice == "2":
                if not check_backend_service():
                    continue
                run_normal_test()
            elif choice == "3":
                if not check_backend_service():
                    continue
                start_web_ui()
            elif choice == "4":
                if not check_backend_service():
                    continue
                run_module_test("auth")
            elif choice == "5":
                if not check_backend_service():
                    continue
                run_module_test("trip")
            elif choice == "6":
                if not check_backend_service():
                    continue
                run_module_test("booking")
            elif choice == "7":
                view_reports()
            elif choice == "8":
                system_check()
            else:
                print("❌ 无效的选择，请输入0-8之间的数字")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
        
        # 等待用户按键继续
        if choice != "0":
            input("\n按回车键继续...")

if __name__ == "__main__":
    # 检查基本环境
    if not check_python_version():
        sys.exit(1)
    
    # 检查是否在正确的目录
    if not os.path.exists("locustfile.py"):
        print("❌ 请在locust_tests目录中运行此脚本")
        sys.exit(1)
    
    # 检查依赖包
    try:
        import locust
    except ImportError:
        print("📦 检测到缺少依赖包，正在安装...")
        if not install_dependencies():
            sys.exit(1)
    
    main() 