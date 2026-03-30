"""
登录页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import PageConfig
import time
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """登录页面"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8080/#/pages/login/login"
        
        # 页面元素定位器 - 适配UniApp
        self.locators = {
            # 输入框
            'phone_input': [
                ('css selector', 'input[placeholder*="手机"], input[type="tel"]'),
                ('css selector', 'input[placeholder*="电话"], input[placeholder*="用户名"]'),
                ('xpath', '//input[@placeholder="手机号" or contains(@placeholder, "电话") or contains(@placeholder, "用户名")]'),
                ('css selector', 'input[maxlength="11"]'),
                ('css selector', 'input[type="text"]:first-of-type')
            ],
            'password_input': [
                ('css selector', 'input[type="password"]'),
                ('css selector', 'input[placeholder*="密码"]'),
                ('xpath', '//input[@type="password" or contains(@placeholder, "密码")]')
            ],
            
            # 按钮
            'login_button': [
                ('css selector', 'button[type="submit"], .login-btn'),
                ('xpath', '//button[contains(text(), "登录") or contains(text(), "提交")]'),
                ('css selector', 'button:last-of-type'),
                ('css selector', '.submit-btn, .btn-primary'),
                ('css selector', 'form button')
            ],
            
            # 注册链接
            'register_link': [
                ('xpath', '//a[contains(text(), "注册") or contains(text(), "没有账号")]'),
                ('css selector', 'a[href*="register"]'),
                ('css selector', '.register-link'),
                ('xpath', '//text()[contains(., "注册")]/..'),
                ('xpath', '//text()[contains(., "没有账号")]/..')
            ]
        }
    
    def navigate_to_login(self):
        """导航到登录页面"""
        self.navigate_to_page(self.url)
    
    def login(self, phone, password):
        """
        用户登录
        
        Args:
            phone (str): 手机号
            password (str): 密码
        
        Returns:
            bool: 登录是否成功
        """
        try:
            logger.info(f"开始登录，手机号: {phone}")
            
            # 填写手机号
            if not self.fill_input_safe('phone_input', phone):
                logger.error("填写手机号失败")
                return False
            
            # 填写密码
            if not self.fill_input_safe('password_input', password):
                logger.error("填写密码失败")
                return False
            
            # 记录当前URL
            current_url = self.get_current_url()
            
            # 点击登录按钮
            if not self.click_element_safe('login_button'):
                logger.error("点击登录按钮失败")
                return False
            
            # 等待页面响应
            time.sleep(2)
            
            # 检查是否登录成功（页面跳转）
            success = self.wait_for_page_change(current_url, timeout=20)
            if success:
                new_url = self.get_current_url()
                logger.info(f"登录成功，页面跳转: {current_url} -> {new_url}")
                return True
            
            # 如果没有页面跳转，检查是否有成功消息
            success_messages = [
                "登录成功", "成功", "欢迎", "Success"
            ]
            page_text = self.get_page_text()
            for msg in success_messages:
                if msg in page_text:
                    logger.info(f"登录成功: {msg}")
                    return True
            
            # 检查是否有错误消息
            error_msg = self.get_error_message()
            if error_msg:
                logger.error(f"登录失败: {error_msg}")
                return False
            
            logger.error("登录失败: 无明确结果")
            return False
            
        except Exception as e:
            logger.error(f"登录过程中出现异常: {e}")
            return False
    
    def fill_input_safe(self, locator_key, value):
        """安全填写输入框"""
        if not value:
            return True
        
        for locator_type, locator_value in self.locators[locator_key]:
            try:
                element = self.find_element_safe((locator_type, locator_value))
                if element:
                    self.clear_and_type(element, value)
                    return True
            except:
                continue
        
        logger.error(f"无法找到输入框: {locator_key}")
        return False
    
    def click_element_safe(self, locator_key):
        """安全点击元素"""
        for locator_type, locator_value in self.locators[locator_key]:
            try:
                element = self.find_element_safe((locator_type, locator_value))
                if element:
                    self.click_element(element)
                    return True
            except:
                continue
        
        logger.error(f"无法点击元素: {locator_key}")
        return False
    
    def click_register_link(self):
        """点击注册链接"""
        return self.click_element_safe('register_link')
    
    def get_error_message(self):
        """获取错误消息"""
        error_selectors = [
            '.error-msg', '.uni-toast', '.toast-message',
            '[class*="error"]', '[class*="toast"]',
            '.message', '.tip'
        ]
        
        for selector in error_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        text = element.text.strip()
                        if text:
                            return text
            except:
                continue
        
        return ""
    
    def get_page_text(self):
        """获取页面文本内容"""
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except:
            return ""
    
    def wait_for_page_change(self, original_url, timeout=10):
        """等待页面跳转"""
        try:
            end_time = time.time() + timeout
            while time.time() < end_time:
                current_url = self.get_current_url()
                if current_url != original_url:
                    return True
                time.sleep(0.5)
            
            logger.error("等待页面跳转超时")
            return False
        except Exception as e:
            logger.error(f"等待页面跳转时出错: {e}")
            return False

    def is_login_page_loaded(self):
        """
        检查登录页面是否加载完成
        
        Returns:
            bool: 是否加载完成
        """
        return (self.is_element_visible(self.locators['phone_input'][0]) and 
                self.is_element_visible(self.locators['password_input'][0]) and 
                self.is_element_visible(self.locators['login_button'][0]))
                
    def get_phone_input_value(self):
        """
        获取手机号输入框的值
        
        Returns:
            str: 手机号输入框的值
        """
        return self.get_element_attribute(self.locators['phone_input'][0], "value")
        
    def get_password_input_value(self):
        """
        获取密码输入框的值
        
        Returns:
            str: 密码输入框的值
        """
        return self.get_element_attribute(self.locators['password_input'][0], "value")
        
    def clear_inputs(self):
        """清空输入框"""
        for locator_type, locator_value in self.locators['phone_input']:
            self.input_text(locator_type, locator_value, clear_first=True)
        for locator_type, locator_value in self.locators['password_input']:
            self.input_text(locator_type, locator_value, clear_first=True) 