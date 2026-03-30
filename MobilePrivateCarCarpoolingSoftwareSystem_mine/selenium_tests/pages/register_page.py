"""
注册页面对象
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from config.config import PageConfig
import time
import logging

logger = logging.getLogger(__name__)

class RegisterPage(BasePage):
    """注册页面"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8080/#/pages/register/register"
        
        # 页面元素定位器 - 适配UniApp
        self.locators = {
            # 基本输入框
            'username_input': [
                ('css selector', 'input[placeholder*="用户名"], input[placeholder*="姓名"]'),
                ('css selector', 'input[type="text"]:first-of-type'),
                ('xpath', '//input[@placeholder="用户名" or contains(@placeholder, "姓名")]'),
                ('css selector', '.uni-input-wrapper input:first-of-type')
            ],
            'phone_input': [
                ('css selector', 'input[placeholder*="手机"], input[type="tel"]'),
                ('css selector', 'input[placeholder*="电话"]'),
                ('xpath', '//input[@placeholder="手机号" or contains(@placeholder, "电话")]'),
                ('css selector', 'input[maxlength="11"]')
            ],
            'password_input': [
                ('css selector', 'input[type="password"]'),
                ('css selector', 'input[placeholder*="密码"]'),
                ('xpath', '//input[@type="password" or contains(@placeholder, "密码")]')
            ],
            'real_name_input': [
                ('css selector', 'input[placeholder*="真实姓名"], input[placeholder*="实名"]'),
                ('css selector', 'input[placeholder*="姓名"]'),
                ('xpath', '//input[contains(@placeholder, "真实") or contains(@placeholder, "实名")]')
            ],
            'id_card_input': [
                ('css selector', 'input[placeholder*="身份证"]'),
                ('css selector', 'input[maxlength="18"]'),
                ('xpath', '//input[contains(@placeholder, "身份证")]')
            ],
            
            # 用户类型选择器 - 多种可能的实现方式
            'user_type_trigger': [
                # UniApp picker触发器
                ('css selector', 'picker[mode="selector"]'),
                ('css selector', '.uni-picker'),
                ('css selector', '[class*="picker"]'),
                # 下拉选择
                ('css selector', 'select'),
                ('css selector', '.select-wrapper'),
                # 按钮或文本触发
                ('css selector', 'button[class*="picker"], .picker-trigger'),
                ('xpath', '//view[contains(@class, "picker") or contains(text(), "选择")]'),
                # 通用文本触发
                ('xpath', '//text()[contains(., "乘客") or contains(., "司机")]/..'),
                ('css selector', '[class*="user-type"], [class*="type-select"]')
            ],
            
            # 用户类型选项
            'passenger_option': [
                ('xpath', '//text()[contains(., "乘客")]/../..'),
                ('css selector', '[value="PASSENGER"], [data-value="PASSENGER"]'),
                ('xpath', '//picker-view-column//text()[contains(., "乘客")]/..'),
                ('css selector', 'option[value="PASSENGER"]')
            ],
            'driver_option': [
                ('xpath', '//text()[contains(., "司机")]/../..'),
                ('css selector', '[value="DRIVER"], [data-value="DRIVER"]'),
                ('xpath', '//picker-view-column//text()[contains(., "司机")]/..'),
                ('css selector', 'option[value="DRIVER"]')
            ],
            
            # 确认按钮
            'confirm_button': [
                ('css selector', '.picker-confirm, .confirm-btn'),
                ('xpath', '//button[contains(text(), "确认") or contains(text(), "确定")]'),
                ('css selector', 'button[class*="confirm"]')
            ],
            
            # 注册按钮
            'register_button': [
                ('css selector', 'button[type="submit"], .register-btn'),
                ('xpath', '//button[contains(text(), "注册") or contains(text(), "提交")]'),
                ('css selector', 'button:last-of-type'),
                ('css selector', '.submit-btn, .btn-primary')
            ],
            
            # 登录链接
            'login_link': [
                ('xpath', '//a[contains(text(), "登录") or contains(text(), "已有账号")]'),
                ('css selector', 'a[href*="login"]'),
                ('css selector', '.login-link')
            ]
        }
    
    def navigate_to_register(self):
        """导航到注册页面"""
        self.navigate_to_page(self.url)
    
    def register(self, user_data):
        """
        注册用户
        
        Args:
            user_data (dict): 用户数据字典
                - username: 用户名
                - phone: 手机号
                - password: 密码
                - realName: 真实姓名
                - idCard: 身份证号
                - userType: 用户类型 (PASSENGER/DRIVER)
        
        Returns:
            bool: 注册是否成功
        """
        try:
            logger.info(f"开始注册用户: {user_data.get('username', '未知')}")
            
            # 填写用户名
            if not self.fill_input_safe('username_input', user_data.get('username', '')):
                logger.error("填写用户名失败")
                return False
            
            # 填写手机号
            if not self.fill_input_safe('phone_input', user_data.get('phone', '')):
                logger.error("填写手机号失败")
                return False
            
            # 填写密码
            if not self.fill_input_safe('password_input', user_data.get('password', '')):
                logger.error("填写密码失败")
                return False
            
            # 填写真实姓名
            if not self.fill_input_safe('real_name_input', user_data.get('realName', '')):
                logger.error("填写真实姓名失败")
                return False
            
            # 填写身份证号
            if not self.fill_input_safe('id_card_input', user_data.get('idCard', '')):
                logger.error("填写身份证号失败")
                return False
            
            # 选择用户类型
            if not self.select_user_type(user_data.get('userType', 'PASSENGER')):
                logger.error("选择用户类型失败")
                return False
            
            # 点击注册按钮
            if not self.click_element_safe('register_button'):
                logger.error("点击注册按钮失败")
                return False
            
            # 等待页面响应
            time.sleep(3)
            
            # 检查是否注册成功（页面跳转或显示成功消息）
            current_url = self.get_current_url()
            if "login" in current_url or "home" in current_url or "index" in current_url:
                logger.info("注册成功，页面已跳转")
                return True
            
            # 检查是否有成功消息
            success_messages = [
                "注册成功", "成功", "欢迎", "Success"
            ]
            page_text = self.get_page_text()
            for msg in success_messages:
                if msg in page_text:
                    logger.info(f"注册成功: {msg}")
                    return True
            
            # 检查是否有错误消息
            error_msg = self.get_error_message()
            if error_msg:
                logger.error(f"注册失败: {error_msg}")
                return False
            
            logger.warning("注册结果不明确")
            return False
            
        except Exception as e:
            logger.error(f"注册过程中出现异常: {e}")
            return False
    
    def select_user_type(self, user_type):
        """
        选择用户类型
        
        Args:
            user_type (str): 用户类型 PASSENGER 或 DRIVER
        
        Returns:
            bool: 选择是否成功
        """
        try:
            # 尝试多种选择方式
            
            # 方式1: 直接查找并点击对应选项
            if user_type == "PASSENGER":
                option_locators = self.locators['passenger_option']
                type_text = "乘客"
            else:
                option_locators = self.locators['driver_option']
                type_text = "司机"
            
            # 先尝试直接点击选项
            for locator_type, locator_value in option_locators:
                try:
                    element = self.find_element_safe((locator_type, locator_value))
                    if element:
                        self.click_element(element)
                        logger.info(f"直接选择用户类型成功: {type_text}")
                        return True
                except:
                    continue
            
            # 方式2: 点击触发器然后选择选项
            trigger_clicked = False
            for locator_type, locator_value in self.locators['user_type_trigger']:
                try:
                    element = self.find_element_safe((locator_type, locator_value))
                    if element:
                        self.click_element(element)
                        trigger_clicked = True
                        time.sleep(1)
                        break
                except:
                    continue
            
            if trigger_clicked:
                # 触发器点击后，再次尝试选择选项
                time.sleep(1)
                for locator_type, locator_value in option_locators:
                    try:
                        element = self.find_element_safe((locator_type, locator_value))
                        if element:
                            self.click_element(element)
                            # 可能需要确认
                            time.sleep(0.5)
                            self.click_element_safe('confirm_button')
                            logger.info(f"通过触发器选择用户类型成功: {type_text}")
                            return True
                    except:
                        continue
            
            # 方式3: 尝试通过文本内容查找
            try:
                # 查找包含用户类型文本的元素
                text_xpath = f'//text()[contains(., "{type_text}")]/..'
                elements = self.driver.find_elements(By.XPATH, text_xpath)
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            self.click_element(element)
                            logger.info(f"通过文本查找选择用户类型成功: {type_text}")
                            return True
                    except:
                        continue
            except:
                pass
            
            # 方式4: 如果是HTML select元素
            try:
                select_element = self.find_element_safe(('css selector', 'select'))
                if select_element:
                    from selenium.webdriver.support.ui import Select
                    select = Select(select_element)
                    select.select_by_value(user_type)
                    logger.info(f"通过select元素选择用户类型成功: {type_text}")
                    return True
            except:
                pass
            
            logger.error(f"所有方式都无法选择用户类型: {type_text}")
            return False
            
        except Exception as e:
            logger.error(f"选择用户类型时出现异常: {e}")
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
    
    def click_login_link(self):
        """点击登录链接"""
        return self.click_element_safe('login_link')
    
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