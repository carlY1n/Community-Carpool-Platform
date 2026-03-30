#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：检查前端页面的实际DOM结构
"""

import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """设置ChromeDriver"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--window-size=375,812')  # iPhone X size
    
    # 移动设备模拟
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # 查找ChromeDriver
    chromedriver_paths = [
        "chromedriver-win64/chromedriver.exe",
        "chromedriver.exe",
        "../chromedriver-win64/chromedriver.exe"
    ]
    
    chromedriver_path = None
    for path in chromedriver_paths:
        if os.path.exists(path):
            chromedriver_path = path
            break
    
    if not chromedriver_path:
        print("未找到ChromeDriver，请确保已安装")
        return None
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def debug_page(driver, url, page_name):
    """调试特定页面"""
    print(f"\n=== 调试页面: {page_name} ===")
    print(f"URL: {url}")
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # 获取页面标题
        title = driver.title
        print(f"页面标题: {title}")
        
        # 获取当前URL
        current_url = driver.current_url
        print(f"当前URL: {current_url}")
        
        # 截图
        screenshot_name = f"debug_{page_name.replace(' ', '_')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"截图保存: {screenshot_name}")
        
        # 检查页面是否加载完成
        try:
            driver.execute_script("return document.readyState") == "complete"
            print("页面加载状态: 完成")
        except:
            print("页面加载状态: 未知")
        
        # 获取页面HTML结构
        try:
            # 查找常见元素
            body = driver.find_element(By.TAG_NAME, "body")
            print(f"页面body元素存在")
            
            # 查找所有输入框
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"找到 {len(inputs)} 个input元素")
            for i, inp in enumerate(inputs[:5]):  # 只显示前5个
                try:
                    input_type = inp.get_attribute("type")
                    placeholder = inp.get_attribute("placeholder")
                    name = inp.get_attribute("name")
                    print(f"  输入框{i+1}: type={input_type}, placeholder={placeholder}, name={name}")
                except:
                    print(f"  输入框{i+1}: 无法获取属性")
            
            # 查找所有按钮
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"找到 {len(buttons)} 个button元素")
            for i, btn in enumerate(buttons[:5]):  # 只显示前5个
                try:
                    text = btn.text
                    btn_type = btn.get_attribute("type")
                    class_name = btn.get_attribute("class")
                    print(f"  按钮{i+1}: text='{text}', type={btn_type}, class={class_name}")
                except:
                    print(f"  按钮{i+1}: 无法获取属性")
            
            # 查找链接
            links = driver.find_elements(By.TAG_NAME, "a")
            print(f"找到 {len(links)} 个链接元素")
            for i, link in enumerate(links[:3]):  # 只显示前3个
                try:
                    text = link.text
                    href = link.get_attribute("href")
                    print(f"  链接{i+1}: text='{text}', href={href}")
                except:
                    print(f"  链接{i+1}: 无法获取属性")
            
            # 查找选择器
            selects = driver.find_elements(By.TAG_NAME, "select")
            if selects:
                print(f"找到 {len(selects)} 个select元素")
            
            # 查找picker相关元素
            pickers = driver.find_elements(By.CSS_SELECTOR, "[class*='picker']")
            if pickers:
                print(f"找到 {len(pickers)} 个picker相关元素")
                for i, picker in enumerate(pickers[:3]):
                    try:
                        class_name = picker.get_attribute("class")
                        print(f"  Picker{i+1}: class={class_name}")
                    except:
                        print(f"  Picker{i+1}: 无法获取属性")
            
            # 查找UniApp相关元素
            uni_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='uni-']")
            if uni_elements:
                print(f"找到 {len(uni_elements)} 个uni-相关元素")
            
            # 检查是否有错误信息
            error_selectors = [
                ".error-msg", ".uni-toast", ".toast-message", 
                "[class*='error']", "[class*='toast']"
            ]
            for selector in error_selectors:
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if error_elements:
                        print(f"找到错误元素 {selector}: {len(error_elements)} 个")
                        for elem in error_elements[:2]:
                            try:
                                text = elem.text
                                if text:
                                    print(f"  错误信息: {text}")
                            except:
                                pass
                except:
                    pass
            
        except Exception as e:
            print(f"分析页面结构时出错: {e}")
        
        # 输出页面HTML（部分）
        try:
            html = driver.page_source
            print(f"页面HTML长度: {len(html)} 字符")
            
            # 保存HTML到文件
            html_file = f"debug_{page_name.replace(' ', '_')}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"页面HTML保存: {html_file}")
            
        except Exception as e:
            print(f"获取页面HTML时出错: {e}")
        
    except Exception as e:
        print(f"访问页面时出错: {e}")

def main():
    """主函数"""
    print("开始调试前端页面结构...")
    
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # 测试页面列表
        pages_to_test = [
            ("http://localhost:8080", "首页"),
            ("http://localhost:8080/#/pages/login/login", "登录页"),
            ("http://localhost:8080/#/pages/register/register", "注册页"),
            ("http://localhost:8080/#/pages/searchTrip/searchTrip", "搜索行程页"),
        ]
        
        for url, page_name in pages_to_test:
            debug_page(driver, url, page_name)
            time.sleep(2)
        
        print("\n=== 调试完成 ===")
        print("请检查生成的截图和HTML文件")
        
    except KeyboardInterrupt:
        print("\n调试被用户中断")
    except Exception as e:
        print(f"调试过程中出错: {e}")
    finally:
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    main() 