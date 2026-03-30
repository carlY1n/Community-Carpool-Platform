#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的测试运行脚本
专门解决当前测试失败的问题
"""

import pytest
import sys
import os

def main():
    """运行简化测试"""
    print("🚀 开始运行简化测试...")
    
    # 测试参数 - 修复类名和方法名
    test_args = [
        "-v",  # 详细输出
        "--tb=short",  # 简短的错误回溯
        "--maxfail=3",  # 最多失败3个就停止
        "--capture=no",  # 不捕获输出，便于调试
        "-x",  # 遇到第一个失败就停止
        "tests/test_config.py::TestConfiguration::test_config_values",  # 修正的测试路径
    ]
    
    # 运行测试
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("✅ 基础配置测试通过，继续运行其他测试...")
        
        # 运行页面配置测试
        page_test_args = [
            "-v",
            "--tb=short",
            "--maxfail=1",
            "tests/test_config.py::TestConfiguration::test_page_config",
        ]
        
        page_result = pytest.main(page_test_args)
        
        if page_result == 0:
            print("✅ 页面配置测试通过，尝试运行实际功能测试...")
            
            # 运行简单的导航测试（不需要登录）
            nav_args = [
                "-v",
                "--tb=short",
                "--maxfail=1",
                "tests/test_user_auth.py::TestUserAuth::test_navigation_between_login_register",
            ]
            
            nav_result = pytest.main(nav_args)
            
            if nav_result == 0:
                print("✅ 页面导航测试通过")
                print("💡 建议：现在可以尝试运行完整的测试套件")
                print("   python run_tests.py")
            else:
                print("❌ 页面导航测试失败")
                print("💡 建议：")
                print("   1. 确保前端服务运行在 localhost:8080")
                print("   2. 运行 python debug_page_structure.py 查看页面结构")
                print("   3. 运行 python quick_fix_tests.py 进行详细诊断")
        else:
            print("❌ 页面配置测试失败")
    
    else:
        print("❌ 基础配置测试失败")
        print("💡 建议：")
        print("   1. 检查配置文件是否正确")
        print("   2. 确保所有依赖都已安装")
        print("   3. 检查 config/config.py 文件")

if __name__ == "__main__":
    main() 