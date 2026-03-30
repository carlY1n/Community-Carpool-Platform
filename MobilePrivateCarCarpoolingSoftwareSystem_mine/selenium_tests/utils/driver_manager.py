"""
WebDriver管理器
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config.config import TestConfig
import logging

class DriverManager:
    """WebDriver管理器"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.logger = logging.getLogger(__name__)
        
    def create_driver(self, headless=False, mobile_emulation=True):
        """
        创建ChromeDriver实例
        
        Args:
            headless (bool): 是否无头模式
            mobile_emulation (bool): 是否启用移动端模拟
        """
        try:
            chrome_options = Options()
            
            # 添加基础选项
            for option in TestConfig.CHROME_OPTIONS:
                chrome_options.add_argument(option)
                
            if headless:
                chrome_options.add_argument("--headless")
            
            # 移动端模拟配置（针对uniapp H5）
            if mobile_emulation:
                mobile_emulation_config = {
                    "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                    "userAgent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) "
                                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 "
                                "Mobile/15E148 Safari/604.1")
                }
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation_config)
            
            # 使用本地ChromeDriver或自动下载
            chromedriver_path = self._get_local_chromedriver_path()
            if chromedriver_path:
                service = Service(chromedriver_path)
                self.logger.info(f"使用本地ChromeDriver: {chromedriver_path}")
            else:
                service = Service(ChromeDriverManager().install())
                self.logger.info("使用自动下载的ChromeDriver")
            
            # 创建driver实例
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
            
            # 创建显式等待对象
            self.wait = WebDriverWait(self.driver, TestConfig.EXPLICIT_WAIT)
            
            self.logger.info("ChromeDriver创建成功")
            return self.driver
            
        except WebDriverException as e:
            self.logger.error(f"创建ChromeDriver失败: {e}")
            raise
            
    def get_driver(self):
        """获取driver实例"""
        if self.driver is None:
            self.create_driver()
        return self.driver
        
    def get_wait(self):
        """获取等待对象"""
        if self.wait is None:
            self.get_driver()
        return self.wait
        
    def quit_driver(self):
        """退出driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("ChromeDriver已退出")
            except Exception as e:
                self.logger.error(f"退出ChromeDriver时出错: {e}")
            finally:
                self.driver = None
                self.wait = None
                
    def take_screenshot(self, filename=None):
        """
        截图
        
        Args:
            filename (str): 截图文件名，不传则使用时间戳
        """
        if not self.driver:
            return None
            
        # 确保截图目录存在
        os.makedirs(TestConfig.SCREENSHOT_DIR, exist_ok=True)
        
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
            
        filepath = os.path.join(TestConfig.SCREENSHOT_DIR, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return None
            
    def wait_for_page_load(self, timeout=20):
        """
        等待页面加载完成
        
        Args:
            timeout (int): 超时时间
        """
        try:
            # 等待document.readyState为complete
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 额外等待一下，确保uniapp渲染完成
            time.sleep(1)
            
        except TimeoutException:
            self.logger.warning("页面加载超时")
            
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        等待元素可点击
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
        """
        timeout = timeout or TestConfig.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"等待元素可点击超时: {locator}")
            raise
            
    def wait_for_element_visible(self, locator, timeout=None):
        """
        等待元素可见
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
        """
        timeout = timeout or TestConfig.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"等待元素可见超时: {locator}")
            raise
            
    def safe_click(self, locator, timeout=None):
        """
        安全点击元素
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            element.click()
            return True
        except Exception as e:
            self.logger.error(f"点击元素失败: {locator}, 错误: {e}")
            return False
            
    def safe_send_keys(self, locator, text, clear_first=True, timeout=None):
        """
        安全输入文本
        
        Args:
            locator (tuple): 元素定位器
            text (str): 输入文本
            clear_first (bool): 是否先清空
            timeout (int): 超时时间
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            self.logger.error(f"输入文本失败: {locator}, 错误: {e}")
            return False
            
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
    def _get_local_chromedriver_path(self):
        """
        获取本地ChromeDriver路径
        
        Returns:
            str: ChromeDriver路径，如果不存在则返回None
        """
        # 从配置获取可能的路径
        possible_paths = TestConfig.get_chromedriver_paths()
        
        for path in possible_paths:
            if path is None:
                continue
                
            full_path = os.path.abspath(path)
            if os.path.exists(full_path):
                self.logger.info(f"找到本地ChromeDriver: {full_path}")
                return full_path
                
        self.logger.info("未找到本地ChromeDriver，将使用自动下载")
        return None 