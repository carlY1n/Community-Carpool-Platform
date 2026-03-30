#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Locust性能测试运行脚本
"""

import os
import sys
import argparse
import subprocess
import time
from datetime import datetime
from config import TestConfig, ScenarioConfig, get_config_from_env

class LocustTestRunner:
    """Locust测试运行器"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.reports_dir = os.path.join(self.base_dir, "reports")
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.reports_dir, self.logs_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def run_test(self, scenario="normal", locustfile="locustfile.py", **kwargs):
        """运行性能测试"""
        print(f"🚀 开始运行性能测试 - 场景: {scenario}")
        
        # 获取场景配置
        scenario_config = self.get_scenario_config(scenario)
        
        # 构建命令
        cmd = self.build_command(locustfile, scenario_config, **kwargs)
        
        print(f"📋 测试配置:")
        print(f"   - 并发用户数: {scenario_config['users']}")
        print(f"   - 启动速率: {scenario_config['spawn_rate']}/秒")
        print(f"   - 运行时间: {scenario_config['run_time']}")
        print(f"   - 目标主机: {kwargs.get('host', TestConfig.HOST)}")
        print(f"   - 测试文件: {locustfile}")
        
        print(f"\n🔧 执行命令: {' '.join(cmd)}")
        
        # 运行测试
        start_time = time.time()
        try:
            result = subprocess.run(cmd, cwd=self.base_dir, check=True)
            end_time = time.time()
            
            print(f"\n✅ 测试完成! 耗时: {end_time - start_time:.2f}秒")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 测试失败: {e}")
            return False
        except KeyboardInterrupt:
            print(f"\n⏹️ 测试被用户中断")
            return False
    
    def get_scenario_config(self, scenario):
        """获取场景配置"""
        scenario_configs = {
            "light": ScenarioConfig.LIGHT_LOAD,
            "normal": ScenarioConfig.NORMAL_LOAD,
            "high": ScenarioConfig.HIGH_LOAD,
            "stress": ScenarioConfig.STRESS_TEST,
            "spike": ScenarioConfig.SPIKE_TEST,
            "stability": ScenarioConfig.STABILITY_TEST
        }
        
        return scenario_configs.get(scenario, ScenarioConfig.NORMAL_LOAD)
    
    def build_command(self, locustfile, scenario_config, **kwargs):
        """构建Locust命令"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        cmd = [
            "locust",
            "-f", locustfile,
            "--host", kwargs.get("host", TestConfig.HOST),
            "--users", str(kwargs.get("users", scenario_config["users"])),
            "--spawn-rate", str(kwargs.get("spawn_rate", scenario_config["spawn_rate"])),
            "--run-time", kwargs.get("run_time", scenario_config["run_time"]),
            "--headless"  # 无头模式
        ]
        
        # 添加报告输出
        if kwargs.get("html_report", True):
            html_file = os.path.join(self.reports_dir, f"report_{timestamp}.html")
            cmd.extend(["--html", html_file])
        
        if kwargs.get("csv_report", True):
            csv_prefix = os.path.join(self.reports_dir, f"stats_{timestamp}")
            cmd.extend(["--csv", csv_prefix])
        
        # 添加日志输出
        if kwargs.get("logfile"):
            cmd.extend(["--logfile", kwargs["logfile"]])
        
        # 添加其他参数
        if kwargs.get("loglevel"):
            cmd.extend(["--loglevel", kwargs["loglevel"]])
        
        return cmd
    
    def run_scenario_tests(self, scenarios=None):
        """运行多个场景测试"""
        if scenarios is None:
            scenarios = ["light", "normal", "high"]
        
        results = {}
        
        for scenario in scenarios:
            print(f"\n{'='*60}")
            print(f"🎯 运行场景: {scenario.upper()}")
            print(f"{'='*60}")
            
            success = self.run_test(scenario=scenario)
            results[scenario] = success
            
            if not success:
                print(f"❌ 场景 {scenario} 测试失败，是否继续？")
                user_input = input("继续测试其他场景？(y/n): ").lower()
                if user_input != 'y':
                    break
            
            # 场景间休息
            if scenario != scenarios[-1]:
                print("⏳ 等待30秒后开始下一个场景...")
                time.sleep(30)
        
        # 输出总结
        print(f"\n{'='*60}")
        print("📊 测试总结")
        print(f"{'='*60}")
        
        for scenario, success in results.items():
            status = "✅ 成功" if success else "❌ 失败"
            print(f"{scenario.ljust(15)}: {status}")
        
        return results
    
    def run_auth_tests(self):
        """运行认证相关测试"""
        return self.run_test(
            scenario="normal",
            locustfile="scenarios/auth_scenario.py",
            users=20,
            run_time="3m"
        )
    
    def run_trip_tests(self):
        """运行行程相关测试"""
        return self.run_test(
            scenario="normal",
            locustfile="scenarios/trip_scenario.py",
            users=30,
            run_time="5m"
        )
    
    def run_booking_tests(self):
        """运行预订相关测试"""
        return self.run_test(
            scenario="normal",
            locustfile="scenarios/booking_scenario.py",
            users=25,
            run_time="4m"
        )
    
    def run_all_module_tests(self):
        """运行所有模块测试"""
        modules = [
            ("认证模块", self.run_auth_tests),
            ("行程模块", self.run_trip_tests),
            ("预订模块", self.run_booking_tests)
        ]
        
        results = {}
        
        for module_name, test_func in modules:
            print(f"\n{'='*60}")
            print(f"🧪 测试模块: {module_name}")
            print(f"{'='*60}")
            
            success = test_func()
            results[module_name] = success
            
            if not success:
                print(f"❌ {module_name} 测试失败")
            else:
                print(f"✅ {module_name} 测试成功")
            
            # 模块间休息
            time.sleep(10)
        
        return results
    
    def run_web_ui(self, **kwargs):
        """运行Web UI模式"""
        print("🌐 启动Locust Web UI...")
        
        cmd = [
            "locust",
            "-f", kwargs.get("locustfile", "locustfile.py"),
            "--host", kwargs.get("host", TestConfig.HOST),
            "--web-port", str(kwargs.get("port", 8089))
        ]
        
        print(f"🔗 Web UI地址: http://localhost:{kwargs.get('port', 8089)}")
        print("按 Ctrl+C 停止服务")
        
        try:
            subprocess.run(cmd, cwd=self.base_dir)
        except KeyboardInterrupt:
            print("\n⏹️ Web UI已停止")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="拼车系统性能测试运行器")
    
    parser.add_argument("--scenario", "-s", 
                       choices=["light", "normal", "high", "stress", "spike", "stability"],
                       default="normal",
                       help="测试场景")
    
    parser.add_argument("--locustfile", "-f",
                       default="locustfile.py",
                       help="Locust测试文件")
    
    parser.add_argument("--host",
                       default=TestConfig.HOST,
                       help="目标主机地址")
    
    parser.add_argument("--users", "-u",
                       type=int,
                       help="并发用户数")
    
    parser.add_argument("--spawn-rate", "-r",
                       type=float,
                       help="用户启动速率")
    
    parser.add_argument("--run-time", "-t",
                       help="运行时间")
    
    parser.add_argument("--web-ui", "-w",
                       action="store_true",
                       help="启动Web UI模式")
    
    parser.add_argument("--port", "-p",
                       type=int,
                       default=8089,
                       help="Web UI端口")
    
    parser.add_argument("--all-scenarios",
                       action="store_true",
                       help="运行所有场景测试")
    
    parser.add_argument("--all-modules",
                       action="store_true",
                       help="运行所有模块测试")
    
    parser.add_argument("--auth-only",
                       action="store_true",
                       help="仅运行认证测试")
    
    parser.add_argument("--trip-only",
                       action="store_true",
                       help="仅运行行程测试")
    
    parser.add_argument("--booking-only",
                       action="store_true",
                       help="仅运行预订测试")
    
    args = parser.parse_args()
    
    runner = LocustTestRunner()
    
    print("🚗 拼车系统性能测试工具")
    print("=" * 50)
    
    try:
        if args.web_ui:
            # Web UI模式
            runner.run_web_ui(
                locustfile=args.locustfile,
                host=args.host,
                port=args.port
            )
        
        elif args.all_scenarios:
            # 运行所有场景
            runner.run_scenario_tests()
        
        elif args.all_modules:
            # 运行所有模块
            runner.run_all_module_tests()
        
        elif args.auth_only:
            # 仅认证测试
            runner.run_auth_tests()
        
        elif args.trip_only:
            # 仅行程测试
            runner.run_trip_tests()
        
        elif args.booking_only:
            # 仅预订测试
            runner.run_booking_tests()
        
        else:
            # 单个场景测试
            kwargs = {
                "host": args.host,
                "locustfile": args.locustfile
            }
            
            if args.users:
                kwargs["users"] = args.users
            if args.spawn_rate:
                kwargs["spawn_rate"] = args.spawn_rate
            if args.run_time:
                kwargs["run_time"] = args.run_time
            
            runner.run_test(scenario=args.scenario, **kwargs)
    
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 