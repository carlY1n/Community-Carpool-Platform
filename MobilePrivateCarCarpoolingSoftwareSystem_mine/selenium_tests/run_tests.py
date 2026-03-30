#!/usr/bin/env python3
"""
测试运行脚本
"""
import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_dependencies():
    """检查依赖是否安装"""
    logger = logging.getLogger(__name__)
    
    try:
        import selenium
        import pytest
        import webdriver_manager
        logger.info("所有依赖已安装")
        return True
    except ImportError as e:
        logger.error(f"缺少依赖: {e}")
        logger.info("请运行: pip install -r requirements.txt")
        return False

def run_tests(args):
    """运行测试"""
    logger = logging.getLogger(__name__)
    
    # 构建pytest命令
    cmd = ["pytest"]
    
    # 添加测试路径
    if args.test_path:
        cmd.append(args.test_path)
    else:
        cmd.append("tests/")
    
    # 添加标记过滤
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    # 添加详细输出
    if args.verbose:
        cmd.append("-v")
    
    # 添加并行执行
    if args.parallel and args.parallel > 1:
        cmd.extend(["-n", str(args.parallel)])
    
    # 添加HTML报告
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/test_report_{timestamp}.html"
        cmd.extend(["--html", report_file, "--self-contained-html"])
        logger.info(f"HTML报告将保存到: {report_file}")
    
    # 添加Allure报告
    if args.allure:
        cmd.extend(["--alluredir", "reports/allure-results"])
        logger.info("Allure报告数据将保存到: reports/allure-results")
    
    # 添加无头模式
    if args.headless:
        cmd.append("--headless")
    
    # 添加基础URL
    if args.base_url:
        cmd.extend(["--base-url", args.base_url])
    
    # 添加其他pytest参数
    if args.pytest_args:
        cmd.extend(args.pytest_args.split())
    
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    # 确保报告目录存在
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # 运行测试
    try:
        result = subprocess.run(cmd, check=False)
        
        if args.allure and result.returncode == 0:
            logger.info("生成Allure报告...")
            subprocess.run(["allure", "generate", "reports/allure-results", "-o", "reports/allure-report", "--clean"])
            logger.info("Allure报告已生成到: reports/allure-report")
            
        return result.returncode
        
    except FileNotFoundError as e:
        logger.error(f"命令未找到: {e}")
        return 1
    except Exception as e:
        logger.error(f"运行测试时出错: {e}")
        return 1

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="拼车系统Selenium功能测试运行器")
    
    # 基本参数
    parser.add_argument("--test-path", "-t", help="测试文件或目录路径")
    parser.add_argument("--markers", "-m", help="pytest标记过滤 (如: smoke, critical)")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--parallel", "-n", type=int, help="并行执行进程数")
    
    # 报告相关
    parser.add_argument("--html-report", action="store_true", help="生成HTML测试报告")
    parser.add_argument("--allure", action="store_true", help="生成Allure报告")
    
    # 浏览器相关
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    parser.add_argument("--base-url", help="测试基础URL (默认: http://localhost:8080)")
    
    # 其他
    parser.add_argument("--pytest-args", help="额外的pytest参数")
    parser.add_argument("--install-deps", action="store_true", help="安装依赖")
    
    args = parser.parse_args()
    
    logger = setup_logging()
    
    # 安装依赖
    if args.install_deps:
        logger.info("安装依赖...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        if result.returncode != 0:
            logger.error("依赖安装失败")
            return 1
        logger.info("依赖安装成功")
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 运行测试
    return run_tests(args)

if __name__ == "__main__":
    sys.exit(main()) 