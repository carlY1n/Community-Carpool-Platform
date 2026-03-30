#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromeDriver自动下载脚本
根据Chrome版本自动下载匹配的ChromeDriver
"""

import os
import sys
import requests
import zipfile
import json
from pathlib import Path
import shutil

def get_chrome_version():
    """获取Chrome版本"""
    try:
        # 从错误信息中我们知道版本是137.0.7151.104
        return "137.0.7151.104"
    except Exception as e:
        print(f"无法获取Chrome版本: {e}")
        return None

def get_chromedriver_version(chrome_version):
    """根据Chrome版本获取对应的ChromeDriver版本"""
    try:
        major_version = chrome_version.split('.')[0]
        
        # Chrome 115+使用新的API
        if int(major_version) >= 115:
            url = f"https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            versions = data.get('versions', [])
            
            # 查找匹配的版本
            for version_info in reversed(versions):  # 从最新版本开始查找
                version = version_info.get('version', '')
                if version.startswith(major_version + '.'):
                    downloads = version_info.get('downloads', {})
                    chromedriver_downloads = downloads.get('chromedriver', [])
                    
                    # 查找Windows平台的下载链接
                    for download in chromedriver_downloads:
                        if download.get('platform') == 'win64':
                            return version, download.get('url')
            
            print(f"未找到Chrome {major_version}版本对应的ChromeDriver")
            return None, None
        else:
            # 旧版本Chrome使用旧API
            url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            driver_version = response.text.strip()
            download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
            return driver_version, download_url
            
    except Exception as e:
        print(f"获取ChromeDriver版本失败: {e}")
        return None, None

def download_chromedriver(download_url, version):
    """下载ChromeDriver"""
    try:
        print(f"正在下载ChromeDriver {version}...")
        response = requests.get(download_url, timeout=300)
        response.raise_for_status()
        
        # 创建临时文件
        zip_path = "chromedriver_temp.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        # 解压文件
        extract_path = "chromedriver_temp"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # 查找chromedriver.exe文件
        chromedriver_exe = None
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file == 'chromedriver.exe':
                    chromedriver_exe = os.path.join(root, file)
                    break
            if chromedriver_exe:
                break
        
        if not chromedriver_exe:
            raise Exception("解压后未找到chromedriver.exe文件")
        
        # 移动到目标目录
        target_dir = Path("chromedriver-win64")
        target_dir.mkdir(exist_ok=True)
        target_path = target_dir / "chromedriver.exe"
        
        # 如果目标文件存在，先备份
        if target_path.exists():
            backup_path = target_dir / "chromedriver_backup.exe"
            shutil.move(str(target_path), str(backup_path))
            print(f"已备份旧版本ChromeDriver到: {backup_path}")
        
        shutil.move(chromedriver_exe, str(target_path))
        
        # 清理临时文件
        os.remove(zip_path)
        shutil.rmtree(extract_path)
        
        print(f"ChromeDriver {version} 下载完成: {target_path}")
        return str(target_path)
        
    except Exception as e:
        print(f"下载ChromeDriver失败: {e}")
        return None

def main():
    """主函数"""
    print("=== ChromeDriver自动下载工具 ===")
    
    # 获取Chrome版本
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("无法获取Chrome版本，请手动指定")
        chrome_version = input("请输入Chrome版本号 (例如: 137.0.7151.104): ").strip()
        if not chrome_version:
            print("未提供Chrome版本号，退出")
            return
    
    print(f"检测到Chrome版本: {chrome_version}")
    
    # 获取对应的ChromeDriver版本和下载链接
    driver_version, download_url = get_chromedriver_version(chrome_version)
    if not driver_version or not download_url:
        print("无法获取匹配的ChromeDriver版本")
        return
    
    print(f"找到匹配的ChromeDriver版本: {driver_version}")
    print(f"下载链接: {download_url}")
    
    # 下载ChromeDriver
    result = download_chromedriver(download_url, driver_version)
    if result:
        print(f"\n✅ ChromeDriver下载成功!")
        print(f"路径: {result}")
        print("\n现在可以运行测试了:")
        print("python -m pytest tests/test_config.py -v")
    else:
        print("\n❌ ChromeDriver下载失败")

if __name__ == "__main__":
    main() 