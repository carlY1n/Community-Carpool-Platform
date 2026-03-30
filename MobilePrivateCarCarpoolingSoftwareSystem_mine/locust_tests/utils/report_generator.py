#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告生成工具
"""

import json
import csv
import os
from datetime import datetime
from jinja2 import Template
import matplotlib.pyplot as plt
import pandas as pd
from config import TestConfig

class ReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, report_dir="reports"):
        self.report_dir = report_dir
        self.ensure_report_dir()
    
    def ensure_report_dir(self):
        """确保报告目录存在"""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_html_report(self, stats_data, test_config=None):
        """生成HTML报告"""
        template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>拼车系统性能测试报告</title>
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1, h2, h3 { color: #333; }
        .header { text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; margin-bottom: 5px; }
        .metric-label { font-size: 0.9em; opacity: 0.9; }
        .table-container { overflow-x: auto; margin-bottom: 30px; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; font-weight: bold; }
        .status-pass { color: #28a745; font-weight: bold; }
        .status-fail { color: #dc3545; font-weight: bold; }
        .chart-container { margin: 20px 0; text-align: center; }
        .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }
        .error-rate { color: #dc3545; font-weight: bold; }
        .success-rate { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 拼车系统性能测试报告</h1>
            <p>测试时间: {{ test_time }}</p>
            {% if test_config %}
            <p>测试配置: {{ test_config.users }}个并发用户, 持续时间{{ test_config.run_time }}</p>
            {% endif %}
        </div>
        
        <div class="summary">
            <div class="metric-card">
                <div class="metric-value">{{ summary.total_requests }}</div>
                <div class="metric-label">总请求数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ "%.2f"|format(summary.avg_response_time) }}ms</div>
                <div class="metric-label">平均响应时间</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ "%.2f"|format(summary.rps) }}</div>
                <div class="metric-label">每秒请求数(RPS)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ "%.2f"|format(summary.error_rate * 100) }}%</div>
                <div class="metric-label">错误率</div>
            </div>
        </div>
        
        <h2>📊 详细统计</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>接口名称</th>
                        <th>请求数</th>
                        <th>失败数</th>
                        <th>错误率</th>
                        <th>平均响应时间(ms)</th>
                        <th>95%响应时间(ms)</th>
                        <th>RPS</th>
                    </tr>
                </thead>
                <tbody>
                    {% for stat in detailed_stats %}
                    <tr>
                        <td>{{ stat.name }}</td>
                        <td>{{ stat.num_requests }}</td>
                        <td>{{ stat.num_failures }}</td>
                        <td class="{% if stat.error_rate > 0.05 %}error-rate{% else %}success-rate{% endif %}">
                            {{ "%.2f"|format(stat.error_rate * 100) }}%
                        </td>
                        <td>{{ "%.2f"|format(stat.avg_response_time) }}</td>
                        <td>{{ "%.2f"|format(stat.response_time_95) }}</td>
                        <td>{{ "%.2f"|format(stat.rps) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <h2>🎯 性能阈值检查</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>检查项</th>
                        <th>阈值</th>
                        <th>实际值</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {% for check in threshold_checks %}
                    <tr>
                        <td>{{ check.name }}</td>
                        <td>{{ check.threshold }}</td>
                        <td>{{ check.actual }}</td>
                        <td class="{% if check.passed %}status-pass{% else %}status-fail{% endif %}">
                            {{ "✅ 通过" if check.passed else "❌ 失败" }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        {% if errors %}
        <h2>❌ 错误详情</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>错误类型</th>
                        <th>出现次数</th>
                        <th>错误信息</th>
                    </tr>
                </thead>
                <tbody>
                    {% for error in errors %}
                    <tr>
                        <td>{{ error.type }}</td>
                        <td>{{ error.count }}</td>
                        <td>{{ error.message }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        
        <h2>📈 测试建议</h2>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            {% for suggestion in suggestions %}
            <p>• {{ suggestion }}</p>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p>报告生成时间: {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
            <p>拼车系统性能测试 - Locust框架</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(template_str)
        
        # 处理统计数据
        summary = self.calculate_summary(stats_data)
        detailed_stats = self.process_detailed_stats(stats_data)
        threshold_checks = self.check_thresholds(summary, detailed_stats)
        errors = self.extract_errors(stats_data)
        suggestions = self.generate_suggestions(summary, detailed_stats, threshold_checks)
        
        html_content = template.render(
            test_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            test_config=test_config,
            summary=summary,
            detailed_stats=detailed_stats,
            threshold_checks=threshold_checks,
            errors=errors,
            suggestions=suggestions,
            datetime=datetime
        )
        
        report_file = os.path.join(self.report_dir, f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file
    
    def calculate_summary(self, stats_data):
        """计算汇总统计"""
        total_requests = sum(stat.get('num_requests', 0) for stat in stats_data)
        total_failures = sum(stat.get('num_failures', 0) for stat in stats_data)
        
        if total_requests > 0:
            error_rate = total_failures / total_requests
            avg_response_time = sum(stat.get('avg_response_time', 0) * stat.get('num_requests', 0) for stat in stats_data) / total_requests
            rps = sum(stat.get('current_rps', 0) for stat in stats_data)
        else:
            error_rate = 0
            avg_response_time = 0
            rps = 0
        
        return {
            'total_requests': total_requests,
            'total_failures': total_failures,
            'error_rate': error_rate,
            'avg_response_time': avg_response_time,
            'rps': rps
        }
    
    def process_detailed_stats(self, stats_data):
        """处理详细统计数据"""
        detailed_stats = []
        
        for stat in stats_data:
            if stat.get('name') and stat.get('name') != 'Aggregated':
                num_requests = stat.get('num_requests', 0)
                num_failures = stat.get('num_failures', 0)
                error_rate = num_failures / num_requests if num_requests > 0 else 0
                
                detailed_stats.append({
                    'name': stat.get('name', ''),
                    'num_requests': num_requests,
                    'num_failures': num_failures,
                    'error_rate': error_rate,
                    'avg_response_time': stat.get('avg_response_time', 0),
                    'response_time_95': stat.get('response_time_95', 0),
                    'rps': stat.get('current_rps', 0)
                })
        
        return detailed_stats
    
    def check_thresholds(self, summary, detailed_stats):
        """检查性能阈值"""
        checks = []
        
        # 检查平均响应时间
        checks.append({
            'name': '平均响应时间',
            'threshold': f"< {TestConfig.PERFORMANCE_THRESHOLDS['response_time_avg']}ms",
            'actual': f"{summary['avg_response_time']:.2f}ms",
            'passed': summary['avg_response_time'] < TestConfig.PERFORMANCE_THRESHOLDS['response_time_avg']
        })
        
        # 检查错误率
        checks.append({
            'name': '错误率',
            'threshold': f"< {TestConfig.PERFORMANCE_THRESHOLDS['error_rate'] * 100}%",
            'actual': f"{summary['error_rate'] * 100:.2f}%",
            'passed': summary['error_rate'] < TestConfig.PERFORMANCE_THRESHOLDS['error_rate']
        })
        
        # 检查RPS
        checks.append({
            'name': '每秒请求数',
            'threshold': f"> {TestConfig.PERFORMANCE_THRESHOLDS['rps_min']}",
            'actual': f"{summary['rps']:.2f}",
            'passed': summary['rps'] > TestConfig.PERFORMANCE_THRESHOLDS['rps_min']
        })
        
        # 检查95%响应时间
        max_95_response_time = max((stat['response_time_95'] for stat in detailed_stats), default=0)
        checks.append({
            'name': '95%响应时间',
            'threshold': f"< {TestConfig.PERFORMANCE_THRESHOLDS['response_time_95']}ms",
            'actual': f"{max_95_response_time:.2f}ms",
            'passed': max_95_response_time < TestConfig.PERFORMANCE_THRESHOLDS['response_time_95']
        })
        
        return checks
    
    def extract_errors(self, stats_data):
        """提取错误信息"""
        errors = []
        
        for stat in stats_data:
            if stat.get('num_failures', 0) > 0:
                errors.append({
                    'type': stat.get('name', 'Unknown'),
                    'count': stat.get('num_failures', 0),
                    'message': stat.get('error_message', '未知错误')
                })
        
        return errors
    
    def generate_suggestions(self, summary, detailed_stats, threshold_checks):
        """生成测试建议"""
        suggestions = []
        
        # 基于错误率的建议
        if summary['error_rate'] > 0.05:
            suggestions.append("错误率较高，建议检查服务器配置和数据库连接")
        
        # 基于响应时间的建议
        if summary['avg_response_time'] > 1000:
            suggestions.append("平均响应时间较长，建议优化数据库查询和缓存策略")
        
        # 基于RPS的建议
        if summary['rps'] < 10:
            suggestions.append("系统吞吐量较低，建议检查服务器性能和网络配置")
        
        # 基于具体接口的建议
        slow_apis = [stat for stat in detailed_stats if stat['avg_response_time'] > 2000]
        if slow_apis:
            api_names = [api['name'] for api in slow_apis[:3]]
            suggestions.append(f"以下接口响应较慢，需要重点优化: {', '.join(api_names)}")
        
        # 基于错误接口的建议
        error_apis = [stat for stat in detailed_stats if stat['error_rate'] > 0.1]
        if error_apis:
            api_names = [api['name'] for api in error_apis[:3]]
            suggestions.append(f"以下接口错误率较高，需要检查业务逻辑: {', '.join(api_names)}")
        
        # 通用建议
        if not suggestions:
            suggestions.append("系统性能表现良好，建议继续监控并定期进行性能测试")
        
        suggestions.append("建议在不同负载下进行多次测试以获得更准确的性能数据")
        suggestions.append("建议结合APM工具进行更深入的性能分析")
        
        return suggestions
    
    def generate_csv_report(self, stats_data):
        """生成CSV报告"""
        csv_file = os.path.join(self.report_dir, f"performance_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow([
                '接口名称', '请求数', '失败数', '错误率(%)', 
                '平均响应时间(ms)', '95%响应时间(ms)', 'RPS'
            ])
            
            # 写入数据
            for stat in stats_data:
                if stat.get('name') and stat.get('name') != 'Aggregated':
                    num_requests = stat.get('num_requests', 0)
                    num_failures = stat.get('num_failures', 0)
                    error_rate = (num_failures / num_requests * 100) if num_requests > 0 else 0
                    
                    writer.writerow([
                        stat.get('name', ''),
                        num_requests,
                        num_failures,
                        f"{error_rate:.2f}",
                        f"{stat.get('avg_response_time', 0):.2f}",
                        f"{stat.get('response_time_95', 0):.2f}",
                        f"{stat.get('current_rps', 0):.2f}"
                    ])
        
        return csv_file
    
    def generate_charts(self, stats_data):
        """生成性能图表"""
        try:
            import matplotlib.pyplot as plt
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 响应时间图表
            self.create_response_time_chart(stats_data)
            
            # 错误率图表
            self.create_error_rate_chart(stats_data)
            
            # RPS图表
            self.create_rps_chart(stats_data)
            
        except ImportError:
            print("matplotlib未安装，跳过图表生成")
    
    def create_response_time_chart(self, stats_data):
        """创建响应时间图表"""
        names = []
        avg_times = []
        p95_times = []
        
        for stat in stats_data:
            if stat.get('name') and stat.get('name') != 'Aggregated':
                names.append(stat.get('name', '')[:20])  # 截断长名称
                avg_times.append(stat.get('avg_response_time', 0))
                p95_times.append(stat.get('response_time_95', 0))
        
        if names:
            fig, ax = plt.subplots(figsize=(12, 6))
            x = range(len(names))
            
            ax.bar([i - 0.2 for i in x], avg_times, 0.4, label='平均响应时间', alpha=0.8)
            ax.bar([i + 0.2 for i in x], p95_times, 0.4, label='95%响应时间', alpha=0.8)
            
            ax.set_xlabel('接口名称')
            ax.set_ylabel('响应时间 (ms)')
            ax.set_title('接口响应时间对比')
            ax.set_xticks(x)
            ax.set_xticklabels(names, rotation=45, ha='right')
            ax.legend()
            
            plt.tight_layout()
            chart_file = os.path.join(self.report_dir, f"response_time_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    
    def create_error_rate_chart(self, stats_data):
        """创建错误率图表"""
        names = []
        error_rates = []
        
        for stat in stats_data:
            if stat.get('name') and stat.get('name') != 'Aggregated':
                num_requests = stat.get('num_requests', 0)
                num_failures = stat.get('num_failures', 0)
                error_rate = (num_failures / num_requests * 100) if num_requests > 0 else 0
                
                names.append(stat.get('name', '')[:20])
                error_rates.append(error_rate)
        
        if names:
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(names, error_rates, alpha=0.8)
            
            # 根据错误率设置颜色
            for i, bar in enumerate(bars):
                if error_rates[i] > 5:
                    bar.set_color('red')
                elif error_rates[i] > 1:
                    bar.set_color('orange')
                else:
                    bar.set_color('green')
            
            ax.set_xlabel('接口名称')
            ax.set_ylabel('错误率 (%)')
            ax.set_title('接口错误率统计')
            ax.set_xticklabels(names, rotation=45, ha='right')
            
            # 添加阈值线
            ax.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='5%阈值')
            ax.legend()
            
            plt.tight_layout()
            chart_file = os.path.join(self.report_dir, f"error_rate_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    
    def create_rps_chart(self, stats_data):
        """创建RPS图表"""
        names = []
        rps_values = []
        
        for stat in stats_data:
            if stat.get('name') and stat.get('name') != 'Aggregated':
                names.append(stat.get('name', '')[:20])
                rps_values.append(stat.get('current_rps', 0))
        
        if names:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(names, rps_values, alpha=0.8, color='skyblue')
            
            ax.set_xlabel('接口名称')
            ax.set_ylabel('每秒请求数 (RPS)')
            ax.set_title('接口RPS统计')
            ax.set_xticklabels(names, rotation=45, ha='right')
            
            plt.tight_layout()
            chart_file = os.path.join(self.report_dir, f"rps_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    
    def generate_json_report(self, stats_data, test_config=None):
        """生成JSON格式报告"""
        summary = self.calculate_summary(stats_data)
        detailed_stats = self.process_detailed_stats(stats_data)
        threshold_checks = self.check_thresholds(summary, detailed_stats)
        
        report_data = {
            'test_info': {
                'test_time': datetime.now().isoformat(),
                'test_config': test_config.__dict__ if test_config else None
            },
            'summary': summary,
            'detailed_stats': detailed_stats,
            'threshold_checks': threshold_checks,
            'test_passed': all(check['passed'] for check in threshold_checks)
        }
        
        json_file = os.path.join(self.report_dir, f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return json_file


def parse_locust_stats(stats_file):
    """解析Locust统计文件"""
    try:
        if stats_file.endswith('.csv'):
            df = pd.read_csv(stats_file)
            stats_data = df.to_dict('records')
        elif stats_file.endswith('.json'):
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)
        else:
            raise ValueError("不支持的文件格式")
        
        return stats_data
    except Exception as e:
        print(f"解析统计文件失败: {e}")
        return []


if __name__ == "__main__":
    # 测试报告生成器
    print("=== 测试报告生成器 ===")
    
    # 模拟测试数据
    mock_stats = [
        {
            'name': '/api/auth/login',
            'num_requests': 1000,
            'num_failures': 5,
            'avg_response_time': 150.5,
            'response_time_95': 300.2,
            'current_rps': 25.5
        },
        {
            'name': '/api/trips/search',
            'num_requests': 800,
            'num_failures': 2,
            'avg_response_time': 200.8,
            'response_time_95': 450.1,
            'current_rps': 20.2
        }
    ]
    
    generator = ReportGenerator()
    
    # 生成HTML报告
    html_file = generator.generate_html_report(mock_stats)
    print(f"HTML报告已生成: {html_file}")
    
    # 生成CSV报告
    csv_file = generator.generate_csv_report(mock_stats)
    print(f"CSV报告已生成: {csv_file}")
    
    # 生成JSON报告
    json_file = generator.generate_json_report(mock_stats)
    print(f"JSON报告已生成: {json_file}") 