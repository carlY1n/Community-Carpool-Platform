#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼车系统性能测试项目安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="carpooling-performance-tests",
    version="1.0.0",
    description="拼车系统性能测试项目 - 基于Locust的专业性能测试解决方案",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Performance Test Team",
    author_email="test@example.com",
    url="https://github.com/example/carpooling-performance-tests",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Benchmark",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "charts": [
            "matplotlib>=3.7.2",
            "seaborn>=0.12.0",
            "plotly>=5.15.0",
        ],
        "monitoring": [
            "psutil>=5.9.0",
            "py-cpuinfo>=9.0.0",
            "GPUtil>=1.4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "carpooling-perf-test=run_tests:main",
            "carpooling-data-gen=utils.data_generator:main",
            "carpooling-report-gen=utils.report_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    zip_safe=False,
    keywords=[
        "performance testing",
        "load testing",
        "locust",
        "api testing",
        "carpooling",
        "stress testing",
        "benchmark"
    ],
    project_urls={
        "Bug Reports": "https://github.com/example/carpooling-performance-tests/issues",
        "Source": "https://github.com/example/carpooling-performance-tests",
        "Documentation": "https://github.com/example/carpooling-performance-tests/wiki",
    },
) 