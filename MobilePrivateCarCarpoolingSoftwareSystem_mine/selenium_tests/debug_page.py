#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页面调试脚本
用于查看页面的实际HTML结构
"""

import time
from utils.driver_manager import DriverManager
from config.config import TestConfig

def debug_login_page():
    """调试登录页面"""
    print("=== 登录页面调试 ===")
    
    # 创建driver
    dm = DriverManager()
    try:
        dm.create_driver(headless=False, mobile_emulation=True)
        driver = dm.driver
        
        # 访问登录页面
        login_url = f"{TestConfig.BASE_URL}/#/pages/login/login"
        print(f"访问页面: {login_url}")
        driver.get(login_url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 获取页面标题
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 获取页面源码
        page_source = driver.page_source
        print(f"页面源码长度: {len(page_source)}")
        
        # 保存页面源码到文件
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("页面源码已保存到: debug_page_source.html")
        
        # 查找可能的输入框
        print("\n=== 查找输入框 ===")
        input_selectors = [
            "input",
            "input[type='text']",
            "input[type='tel']",
            "input[type='password']",
            ".uni-input-input",
            ".uni-input",
            "[class*='input']",
            "[placeholder*='手机']",
            "[placeholder*='密码']",
            "[placeholder*='phone']",
            "[placeholder*='password']"
        ]
        
        for selector in input_selectors:
            try:
                elements = driver.find_elements("css selector", selector)
                if elements:
                    print(f"找到 {len(elements)} 个元素: {selector}")
                    for i, elem in enumerate(elements):
                        try:
                            placeholder = elem.get_attribute("placeholder") or ""
                            type_attr = elem.get_attribute("type") or ""
                            class_attr = elem.get_attribute("class") or ""
                            print(f"  [{i}] placeholder='{placeholder}', type='{type_attr}', class='{class_attr}'")
                        except Exception as e:
                            print(f"  [{i}] 获取属性失败: {e}")
            except Exception as e:
                print(f"查找失败 {selector}: {e}")
        
        # 查找可能的按钮
        print("\n=== 查找按钮 ===")
        button_selectors = [
            "button",
            ".uni-button",
            "[class*='button']",
            "[class*='btn']",
            "view[class*='button']",
            "text[class*='button']"
        ]
        
        for selector in button_selectors:
            try:
                elements = driver.find_elements("css selector", selector)
                if elements:
                    print(f"找到 {len(elements)} 个元素: {selector}")
                    for i, elem in enumerate(elements):
                        try:
                            text = elem.text or ""
                            class_attr = elem.get_attribute("class") or ""
                            print(f"  [{i}] text='{text}', class='{class_attr}'")
                        except Exception as e:
                            print(f"  [{i}] 获取属性失败: {e}")
            except Exception as e:
                print(f"查找失败 {selector}: {e}")
        
        # 截图
        screenshot_path = dm.take_screenshot("debug_login_page.png")
        print(f"\n截图已保存: {screenshot_path}")
        
        # 等待用户查看
        input("\n按回车键继续...")
        
    except Exception as e:
        print(f"调试过程中出错: {e}")
    finally:
        dm.quit_driver()

if __name__ == "__main__":
    debug_login_page() 