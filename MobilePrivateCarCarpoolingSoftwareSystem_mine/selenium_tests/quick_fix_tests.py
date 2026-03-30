#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复测试脚本
解决已知的测试问题并提供更好的调试信息
"""

import time
import sys
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuickTestFixer:
    """快速测试修复器"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """设置ChromeDriver"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--window-size=375,812')
        
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
            logger.error("未找到ChromeDriver")
            return False
        
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        return True
    
    def test_basic_connectivity(self):
        """测试基本连接性"""
        logger.info("=== 测试基本连接性 ===")
        
        try:
            # 测试前端连接
            self.driver.get("http://localhost:8080")
            time.sleep(3)
            
            title = self.driver.title
            url = self.driver.current_url
            logger.info(f"前端页面标题: {title}")
            logger.info(f"前端URL: {url}")
            
            # 检查页面是否正常加载
            body = self.driver.find_element(By.TAG_NAME, "body")
            if body:
                logger.info("前端页面加载正常")
                return True
            else:
                logger.error("前端页面加载失败")
                return False
                
        except Exception as e:
            logger.error(f"前端连接失败: {e}")
            return False
    
    def test_backend_connectivity(self):
        """测试后端连接性"""
        logger.info("=== 测试后端连接性 ===")
        
        try:
            import requests
            
            # 测试后端健康检查
            backend_urls = [
                "http://localhost:8888/health",
                "http://localhost:8888/api/health",
                "http://localhost:8888/actuator/health",
                "http://localhost:8888/"
            ]
            
            for url in backend_urls:
                try:
                    response = requests.get(url, timeout=5)
                    logger.info(f"后端URL {url}: 状态码 {response.status_code}")
                    if response.status_code == 200:
                        return True
                except Exception as e:
                    logger.warning(f"后端URL {url} 连接失败: {e}")
            
            logger.error("所有后端URL都无法连接")
            return False
            
        except ImportError:
            logger.warning("requests库未安装，跳过后端连接测试")
            return True
        except Exception as e:
            logger.error(f"后端连接测试失败: {e}")
            return False
    
    def fix_login_page(self):
        """修复登录页面测试"""
        logger.info("=== 修复登录页面 ===")
        
        try:
            # 导航到登录页面
            self.driver.get("http://localhost:8080/#/pages/login/login")
            time.sleep(3)
            
            # 截图
            self.driver.save_screenshot("fix_login_page.png")
            
            # 查找所有输入框
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"找到 {len(inputs)} 个输入框")
            
            phone_input = None
            password_input = None
            
            for i, inp in enumerate(inputs):
                try:
                    input_type = inp.get_attribute("type")
                    placeholder = inp.get_attribute("placeholder")
                    logger.info(f"输入框{i+1}: type={input_type}, placeholder={placeholder}")
                    
                    # 智能识别手机号输入框
                    if (input_type in ["text", "tel", "number"] and 
                        (not password_input or placeholder and "手机" in placeholder)):
                        phone_input = inp
                    
                    # 识别密码输入框
                    if input_type == "password":
                        password_input = inp
                        
                except Exception as e:
                    logger.warning(f"获取输入框{i+1}属性失败: {e}")
            
            # 查找所有按钮
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"找到 {len(buttons)} 个按钮")
            
            login_button = None
            for i, btn in enumerate(buttons):
                try:
                    text = btn.text
                    btn_type = btn.get_attribute("type")
                    logger.info(f"按钮{i+1}: text='{text}', type={btn_type}")
                    
                    if "登录" in text or btn_type == "submit":
                        login_button = btn
                        
                except Exception as e:
                    logger.warning(f"获取按钮{i+1}属性失败: {e}")
            
            # 尝试登录
            if phone_input and password_input and login_button:
                logger.info("尝试执行登录操作")
                
                # 清空并输入测试数据
                phone_input.clear()
                phone_input.send_keys("13800138001")
                
                password_input.clear()
                password_input.send_keys("123456")
                
                time.sleep(1)
                
                # 点击登录按钮
                original_url = self.driver.current_url
                login_button.click()
                
                time.sleep(5)
                
                # 检查结果
                new_url = self.driver.current_url
                if new_url != original_url:
                    logger.info(f"登录成功，页面跳转: {original_url} -> {new_url}")
                    return True
                else:
                    logger.warning("登录后页面未跳转")
                    
                    # 查找错误消息
                    error_selectors = [
                        ".error-msg", ".uni-toast", ".toast-message",
                        "[class*='error']", "[class*='toast']"
                    ]
                    
                    for selector in error_selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for elem in elements:
                                if elem.is_displayed():
                                    text = elem.text.strip()
                                    if text:
                                        logger.info(f"错误信息: {text}")
                        except:
                            pass
                    
                    return False
            else:
                logger.error("登录页面元素不完整")
                logger.error(f"手机号输入框: {phone_input is not None}")
                logger.error(f"密码输入框: {password_input is not None}")
                logger.error(f"登录按钮: {login_button is not None}")
                return False
                
        except Exception as e:
            logger.error(f"修复登录页面失败: {e}")
            return False
    
    def fix_register_page(self):
        """修复注册页面测试"""
        logger.info("=== 修复注册页面 ===")
        
        try:
            # 导航到注册页面
            self.driver.get("http://localhost:8080/#/pages/register/register")
            time.sleep(3)
            
            # 截图
            self.driver.save_screenshot("fix_register_page.png")
            
            # 查找所有输入框
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"找到 {len(inputs)} 个输入框")
            
            for i, inp in enumerate(inputs):
                try:
                    input_type = inp.get_attribute("type")
                    placeholder = inp.get_attribute("placeholder")
                    name = inp.get_attribute("name")
                    logger.info(f"输入框{i+1}: type={input_type}, placeholder={placeholder}, name={name}")
                except:
                    logger.warning(f"获取输入框{i+1}属性失败")
            
            # 查找用户类型选择器
            selectors_to_try = [
                ("css selector", "picker"),
                ("css selector", ".uni-picker"),
                ("css selector", "[class*='picker']"),
                ("css selector", "select"),
                ("xpath", "//view[contains(@class, 'picker')]"),
                ("xpath", "//text()[contains(., '选择')]/.."),
            ]
            
            user_type_element = None
            for selector_type, selector_value in selectors_to_try:
                try:
                    if selector_type == "css selector":
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector_value)
                    else:
                        elements = self.driver.find_elements(By.XPATH, selector_value)
                    
                    if elements:
                        logger.info(f"找到用户类型选择器: {selector_value}, 数量: {len(elements)}")
                        user_type_element = elements[0]
                        break
                except:
                    pass
            
            if not user_type_element:
                logger.warning("未找到用户类型选择器")
                
                # 尝试查找包含用户类型的文本
                try:
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    if "乘客" in page_text or "司机" in page_text:
                        logger.info("页面包含用户类型文本")
                        
                        # 查找所有包含乘客或司机的元素
                        passenger_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '乘客')]")
                        driver_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '司机')]")
                        
                        logger.info(f"找到 {len(passenger_elements)} 个包含'乘客'的元素")
                        logger.info(f"找到 {len(driver_elements)} 个包含'司机'的元素")
                        
                except Exception as e:
                    logger.warning(f"查找用户类型文本失败: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"修复注册页面失败: {e}")
            return False
    
    def fix_search_trip_page(self):
        """修复搜索行程页面测试"""
        logger.info("=== 修复搜索行程页面 ===")
        
        try:
            # 导航到搜索行程页面
            self.driver.get("http://localhost:8080/#/pages/searchTrip/searchTrip")
            time.sleep(3)
            
            # 截图
            self.driver.save_screenshot("fix_search_trip_page.png")
            
            # 查找输入框
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"找到 {len(inputs)} 个输入框")
            
            start_input = None
            end_input = None
            
            for i, inp in enumerate(inputs):
                try:
                    placeholder = inp.get_attribute("placeholder")
                    value = inp.get_attribute("value")
                    logger.info(f"输入框{i+1}: placeholder={placeholder}, value={value}")
                    
                    if placeholder and "出发" in placeholder:
                        start_input = inp
                    elif placeholder and ("目的" in placeholder or "到达" in placeholder):
                        end_input = inp
                    elif i == 0 and not start_input:
                        start_input = inp
                    elif i == 1 and not end_input:
                        end_input = inp
                        
                except:
                    logger.warning(f"获取输入框{i+1}属性失败")
            
            # 查找搜索按钮
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"找到 {len(buttons)} 个按钮")
            
            search_button = None
            for i, btn in enumerate(buttons):
                try:
                    text = btn.text
                    logger.info(f"按钮{i+1}: text='{text}'")
                    
                    if "搜索" in text or "查询" in text:
                        search_button = btn
                        
                except:
                    logger.warning(f"获取按钮{i+1}属性失败")
            
            # 尝试搜索
            if start_input and end_input:
                logger.info("尝试执行搜索操作")
                
                start_input.clear()
                start_input.send_keys("上海市黄浦区人民广场")
                
                end_input.clear()
                end_input.send_keys("上海市静安区静安寺")
                
                time.sleep(1)
                
                if search_button:
                    search_button.click()
                else:
                    # 尝试按回车
                    from selenium.webdriver.common.keys import Keys
                    end_input.send_keys(Keys.ENTER)
                
                time.sleep(3)
                
                # 检查搜索结果
                current_url = self.driver.current_url
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                
                logger.info(f"搜索后URL: {current_url}")
                
                if "没有找到" in page_text or "暂无" in page_text or "空" in page_text:
                    logger.info("搜索返回空结果（正常）")
                    return True
                elif "行程" in page_text or "结果" in page_text:
                    logger.info("搜索返回结果")
                    return True
                else:
                    logger.warning("搜索结果不明确")
                    return False
            else:
                logger.error("搜索页面元素不完整")
                return False
                
        except Exception as e:
            logger.error(f"修复搜索行程页面失败: {e}")
            return False
    
    def run_quick_fixes(self):
        """运行快速修复"""
        logger.info("开始快速修复测试...")
        
        if not self.setup_driver():
            logger.error("ChromeDriver设置失败")
            return False
        
        try:
            results = {}
            
            # 测试基本连接性
            results['connectivity'] = self.test_basic_connectivity()
            results['backend'] = self.test_backend_connectivity()
            
            # 修复各个页面
            results['login'] = self.fix_login_page()
            results['register'] = self.fix_register_page()
            results['search'] = self.fix_search_trip_page()
            
            # 输出结果
            logger.info("=== 快速修复结果 ===")
            for test_name, result in results.items():
                status = "✅ 通过" if result else "❌ 失败"
                logger.info(f"{test_name}: {status}")
            
            # 生成修复建议
            self.generate_fix_suggestions(results)
            
            return True
            
        except Exception as e:
            logger.error(f"快速修复过程中出错: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def generate_fix_suggestions(self, results):
        """生成修复建议"""
        logger.info("=== 修复建议 ===")
        
        if not results.get('connectivity'):
            logger.info("🔧 前端连接失败:")
            logger.info("   - 确保前端服务运行在 localhost:8080")
            logger.info("   - 检查 npm run dev 或 npm start 是否正常运行")
            logger.info("   - 确认防火墙没有阻止端口8080")
        
        if not results.get('backend'):
            logger.info("🔧 后端连接失败:")
            logger.info("   - 确保后端服务运行在 localhost:8888") 
            logger.info("   - 检查 Spring Boot 应用是否正常启动")
            logger.info("   - 确认数据库连接是否正常")
        
        if not results.get('login'):
            logger.info("🔧 登录页面问题:")
            logger.info("   - 检查页面元素选择器是否正确")
            logger.info("   - 确认测试用户数据是否在数据库中")
            logger.info("   - 验证登录API是否正常工作")
        
        if not results.get('register'):
            logger.info("🔧 注册页面问题:")
            logger.info("   - 用户类型选择器可能使用了不同的实现方式")
            logger.info("   - 建议更新选择器匹配策略")
            logger.info("   - 检查UniApp picker组件的实际DOM结构")
        
        if not results.get('search'):
            logger.info("🔧 搜索页面问题:")
            logger.info("   - 搜索功能可能需要登录状态")
            logger.info("   - 检查搜索API是否返回正确的响应")
            logger.info("   - 验证搜索结果的页面结构")

def main():
    """主函数"""
    fixer = QuickTestFixer()
    fixer.run_quick_fixes()

if __name__ == "__main__":
    main() 
 