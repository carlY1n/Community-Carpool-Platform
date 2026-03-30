"""
页面对象模型基类
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, 
    ElementNotInteractableException, StaleElementReferenceException
)
from config.config import TestConfig, PageConfig
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """页面基类"""
    
    def __init__(self, driver_manager):
        """
        初始化页面
        
        Args:
            driver_manager: DriverManager实例
        """
        self.driver_manager = driver_manager
        self.driver = driver_manager.get_driver()
        self.wait = driver_manager.get_wait()
        self.short_wait = WebDriverWait(self.driver, 3)
        self.long_wait = WebDriverWait(self.driver, 30)
        self.logger = logging.getLogger(__name__)
        
    def navigate_to_page(self, page_path):
        """
        导航到指定页面
        
        Args:
            page_path (str): 页面路径
        """
        url = f"{TestConfig.BASE_URL}/#" + page_path
        self.logger.info(f"导航到页面: {url}")
        self.driver.get(url)
        self.driver_manager.wait_for_page_load()
        
    def get_current_url(self):
        """获取当前URL"""
        try:
            return self.driver.current_url
        except Exception as e:
            self.logger.error(f"获取当前URL失败: {e}")
            return ""
        
    def get_page_title(self):
        """获取页面标题"""
        try:
            return self.driver.title
        except Exception as e:
            self.logger.error(f"获取页面标题失败: {e}")
            return ""
        
    def wait_for_toast_message(self, timeout=5):
        """
        等待并获取toast消息
        
        Args:
            timeout (int): 超时时间
            
        Returns:
            str: toast消息内容，如果没有则返回None
        """
        try:
            # uniapp的toast通常使用uni-toast类
            toast_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".uni-toast, .toast, [class*='toast']"))
            )
            return toast_element.text
        except TimeoutException:
            return None
            
    def wait_for_loading_complete(self, timeout=10):
        """
        等待加载完成
        
        Args:
            timeout (int): 超时时间
        """
        try:
            # 等待loading消失
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".uni-loading, .loading, [class*='loading']"))
            )
        except TimeoutException:
            self.logger.warning("等待loading完成超时")
            
    def scroll_to_element(self, locator):
        """
        滚动到指定元素
        
        Args:
            locator (tuple): 元素定位器
        """
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
        except NoSuchElementException:
            self.logger.error(f"滚动到元素失败，元素不存在: {locator}")
            
    def is_element_present(self, locator, timeout=5):
        """
        检查元素是否存在
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
            
        Returns:
            bool: 元素是否存在
        """
        try:
            self.short_wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
            
    def is_element_visible(self, locator, timeout=5):
        """
        检查元素是否可见
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
            
        Returns:
            bool: 元素是否可见
        """
        try:
            self.short_wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
            
    def get_element_text(self, locator, timeout=10):
        """
        获取元素文本
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
            
        Returns:
            str: 元素文本
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element.text.strip()
        except TimeoutException:
            self.logger.error(f"获取元素文本超时: {locator}")
            return ""
            
    def get_element_attribute(self, locator, attribute_name, timeout=10):
        """
        获取元素属性
        
        Args:
            locator (tuple): 元素定位器
            attribute_name (str): 属性名
            timeout (int): 超时时间
            
        Returns:
            str: 属性值
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element.get_attribute(attribute_name)
        except TimeoutException:
            self.logger.error(f"获取元素属性超时: {locator}, 属性: {attribute_name}")
            return ""
            
    def click_element(self, locator, timeout=10):
        """
        点击元素
        
        Args:
            locator (tuple): 元素定位器
            timeout (int): 超时时间
            
        Returns:
            bool: 是否点击成功
        """
        return self.driver_manager.safe_click(locator, timeout)
        
    def input_text(self, locator, text, clear_first=True, timeout=10):
        """
        输入文本
        
        Args:
            locator (tuple): 元素定位器
            text (str): 输入文本
            clear_first (bool): 是否先清空
            timeout (int): 超时时间
            
        Returns:
            bool: 是否输入成功
        """
        return self.driver_manager.safe_send_keys(locator, text, clear_first, timeout)
        
    def wait_for_page_change(self, original_url, timeout=10):
        """
        等待页面跳转
        
        Args:
            original_url (str): 原始URL
            timeout (int): 超时时间
            
        Returns:
            bool: 是否跳转成功
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != original_url
            )
            self.driver_manager.wait_for_page_load()
            return True
        except TimeoutException:
            self.logger.error("等待页面跳转超时")
            return False
            
    def go_back(self):
        """返回上一页"""
        self.driver.back()
        self.driver_manager.wait_for_page_load()
        
    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
        self.driver_manager.wait_for_page_load()
        
    def take_screenshot(self, filename=None):
        """截图"""
        return self.driver_manager.take_screenshot(filename)

    def find_element_safe(self, locator, timeout=10):
        """安全查找元素"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.debug(f"查找元素超时: {locator}")
            return None
        except Exception as e:
            logger.debug(f"查找元素失败: {locator}, 错误: {e}")
            return None

    def find_elements_safe(self, locator, timeout=5):
        """安全查找多个元素"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.debug(f"查找元素超时: {locator}")
            return []
        except Exception as e:
            logger.debug(f"查找元素失败: {locator}, 错误: {e}")
            return []

    def wait_for_element_clickable(self, locator, timeout=10):
        """等待元素可点击"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            logger.error(f"等待元素可点击超时: {locator}")
            return None
        except Exception as e:
            logger.error(f"等待元素可点击失败: {locator}, 错误: {e}")
            return None

    def click_element(self, element):
        """点击元素"""
        try:
            if element.is_displayed() and element.is_enabled():
                element.click()
                return True
            else:
                logger.error("元素不可见或不可用")
                return False
        except ElementNotInteractableException:
            logger.warning("元素不可交互，尝试JavaScript点击")
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                logger.error(f"JavaScript点击失败: {e}")
                return False
        except Exception as e:
            logger.error(f"点击元素失败: {e}")
            return False

    def click_element_by_locator(self, locator, timeout=10):
        """通过定位器点击元素"""
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            if element:
                return self.click_element(element)
            else:
                logger.error(f"点击元素失败: {locator}, 错误: {e}")
                return False
        except Exception as e:
            logger.error(f"点击元素失败: {locator}, 错误: {e}")
            return False

    def clear_and_type(self, element, text):
        """清空并输入文本"""
        try:
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            return False

    def type_text_by_locator(self, locator, text, timeout=10):
        """通过定位器输入文本"""
        try:
            element = self.find_element_safe(locator, timeout)
            if element:
                return self.clear_and_type(element, text)
            else:
                logger.error(f"找不到输入框: {locator}")
                return False
        except Exception as e:
            logger.error(f"输入文本失败: {locator}, 错误: {e}")
            return False

    def scroll_to_bottom(self):
        """滚动到页面底部"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"滚动到底部失败: {e}")
            return False

    def scroll_to_top(self):
        """滚动到页面顶部"""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"滚动到顶部失败: {e}")
            return False

    def switch_to_alert(self, timeout=10):
        """切换到弹窗"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            return alert
        except TimeoutException:
            logger.warning("没有弹窗出现")
            return None

    def accept_alert(self, timeout=10):
        """接受弹窗"""
        try:
            alert = self.switch_to_alert(timeout)
            if alert:
                alert.accept()
                return True
            return False
        except Exception as e:
            logger.error(f"接受弹窗失败: {e}")
            return False

    def dismiss_alert(self, timeout=10):
        """取消弹窗"""
        try:
            alert = self.switch_to_alert(timeout)
            if alert:
                alert.dismiss()
                return True
            return False
        except Exception as e:
            logger.error(f"取消弹窗失败: {e}")
            return False

    def get_alert_text(self, timeout=10):
        """获取弹窗文本"""
        try:
            alert = self.switch_to_alert(timeout)
            if alert:
                return alert.text
            return ""
        except Exception as e:
            logger.error(f"获取弹窗文本失败: {e}")
            return ""

    def execute_javascript(self, script, *args):
        """执行JavaScript"""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"执行JavaScript失败: {e}")
            return None

    def go_forward(self):
        """前进到下一页"""
        try:
            self.driver.forward()
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"前进失败: {e}")
            return False

    def wait_for_url_change(self, current_url, timeout=10):
        """等待URL变化"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: driver.current_url != current_url)
            return True
        except TimeoutException:
            logger.warning("URL未发生变化")
            return False

    def wait_for_url_contains(self, text, timeout=10):
        """等待URL包含指定文本"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_contains(text))
            return True
        except TimeoutException:
            logger.warning(f"URL不包含: {text}")
            return False

    def get_page_source(self):
        """获取页面源码"""
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"获取页面源码失败: {e}")
            return ""

    def hover_over_element(self, element):
        """鼠标悬停"""
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"鼠标悬停失败: {e}")
            return False

    def double_click_element(self, element):
        """双击元素"""
        try:
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            return True
        except Exception as e:
            logger.error(f"双击失败: {e}")
            return False

    def right_click_element(self, element):
        """右击元素"""
        try:
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()
            return True
        except Exception as e:
            logger.error(f"右击失败: {e}")
            return False

    def send_keys_to_element(self, element, keys):
        """向元素发送按键"""
        try:
            element.send_keys(keys)
            return True
        except Exception as e:
            logger.error(f"发送按键失败: {e}")
            return False

    def press_enter(self, element):
        """按回车键"""
        return self.send_keys_to_element(element, Keys.ENTER)

    def press_escape(self, element):
        """按ESC键"""
        return self.send_keys_to_element(element, Keys.ESCAPE)

    def press_tab(self, element):
        """按Tab键"""
        return self.send_keys_to_element(element, Keys.TAB)

    def wait_and_retry(self, func, max_retries=3, delay=1):
        """等待并重试操作"""
        for attempt in range(max_retries):
            try:
                result = func()
                if result:
                    return True
            except Exception as e:
                logger.warning(f"第{attempt + 1}次尝试失败: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(delay)
        
        logger.error(f"操作失败，已重试{max_retries}次")
        return False 