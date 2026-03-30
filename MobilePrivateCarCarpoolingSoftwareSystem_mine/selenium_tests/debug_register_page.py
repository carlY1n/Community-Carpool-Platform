#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册页面调试脚本
用于查看注册页面的实际HTML结构
"""

import time
from utils.driver_manager import DriverManager
from config.config import TestConfig

def debug_register_page():
    """调试注册页面"""
    print("=== 注册页面调试 ===")
    
    # 创建driver
    dm = DriverManager()
    try:
        dm.create_driver(headless=False, mobile_emulation=True)
        driver = dm.driver
        
        # 访问注册页面
        register_url = f"{TestConfig.BASE_URL}/#/pages/register/register"
        print(f"访问页面: {register_url}")
        driver.get(register_url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 获取页面标题
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 查找可能的输入框
        print("\n=== 查找输入框 ===")
        input_selectors = [
            "input",
            "input[type='text']",
            "input[type='tel']",
            "input[type='password']",
            ".uni-input-input",
            ".uni-input",
            "[class*='input']"
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
        
        # 查找选择器（用户类型选择）
        print("\n=== 查找选择器 ===")
        select_selectors = [
            "picker",
            ".uni-picker",
            "[class*='picker']",
            "select",
            "[class*='select']"
        ]
        
        for selector in select_selectors:
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
        screenshot_path = dm.take_screenshot("debug_register_page.png")
        print(f"\n截图已保存: {screenshot_path}")
        
        # 等待用户查看
        input("\n按回车键继续...")
        
    except Exception as e:
        print(f"调试过程中出错: {e}")
    finally:
        dm.quit_driver()

if __name__ == "__main__":
    debug_register_page() 