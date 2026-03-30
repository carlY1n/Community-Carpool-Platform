"""
行程相关页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import PageConfig, TestConfig
import time

class SearchTripPage(BasePage):
    """搜索行程页面"""
    
    # 搜索表单元素 - 根据实际页面结构更新
    START_LOCATION_INPUT = (By.CSS_SELECTOR, "input[type='text'].uni-input-input:first-of-type")  # 第一个输入框
    END_LOCATION_INPUT = (By.CSS_SELECTOR, "input[type='text'].uni-input-input:last-of-type")  # 第二个输入框
    DEPARTURE_TIME_PICKER = (By.CSS_SELECTOR, ".picker-label, .picker-value")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-btn")
    
    # 搜索结果
    TRIP_LIST = (By.CSS_SELECTOR, ".trip-list, .result-list")
    TRIP_ITEM = (By.CSS_SELECTOR, ".trip-item, .trip-card")
    TRIP_ITEM_DRIVER = (By.CSS_SELECTOR, ".trip-item .driver-name, .trip-card .driver")
    TRIP_ITEM_PRICE = (By.CSS_SELECTOR, ".trip-item .price, .trip-card .price")
    TRIP_ITEM_TIME = (By.CSS_SELECTOR, ".trip-item .time, .trip-card .departure-time")
    BOOK_BUTTON = (By.CSS_SELECTOR, ".trip-item .book-btn, .trip-card .book")
    
    # 空状态
    EMPTY_STATE = (By.CSS_SELECTOR, ".empty-state, .no-result")
    
    def __init__(self, driver_manager):
        """初始化搜索行程页面"""
        super().__init__(driver_manager)
        
    def navigate_to_search_trip(self):
        """导航到搜索行程页面"""
        self.navigate_to_page(PageConfig.PAGES["search_trip"])
        
    def input_start_location(self, location):
        """
        输入出发地
        
        Args:
            location (str): 出发地
            
        Returns:
            bool: 是否输入成功
        """
        return self.input_text(self.START_LOCATION_INPUT, location)
        
    def input_end_location(self, location):
        """
        输入目的地
        
        Args:
            location (str): 目的地
            
        Returns:
            bool: 是否输入成功
        """
        return self.input_text(self.END_LOCATION_INPUT, location)
        
    def select_departure_time(self, time_str):
        """
        选择出发时间
        
        Args:
            time_str (str): 时间字符串
            
        Returns:
            bool: 是否选择成功
        """
        try:
            # 点击时间选择器
            if not self.click_element(self.DEPARTURE_TIME_PICKER):
                return False
                
            # 这里需要根据实际的时间选择器实现来调整
            # 通常uniapp的时间选择器会弹出picker
            time.sleep(1)
            
            # 选择确认按钮（具体实现需要根据实际页面调整）
            confirm_btn = (By.CSS_SELECTOR, ".picker-confirm, .confirm-btn")
            return self.click_element(confirm_btn)
            
        except Exception as e:
            self.logger.error(f"选择出发时间失败: {e}")
            return False
            
    def click_search_button(self):
        """
        点击搜索按钮
        
        Returns:
            bool: 是否点击成功
        """
        return self.click_element(self.SEARCH_BUTTON)
        
    def search_trips(self, start_location, end_location, departure_time=None):
        """
        搜索行程
        
        Args:
            start_location (str): 出发地
            end_location (str): 目的地
            departure_time (str): 出发时间，可选
            
        Returns:
            bool: 是否搜索成功
        """
        self.logger.info(f"搜索行程：{start_location} -> {end_location}")
        
        # 输入出发地
        if not self.input_start_location(start_location):
            self.logger.error("输入出发地失败")
            return False
            
        # 输入目的地
        if not self.input_end_location(end_location):
            self.logger.error("输入目的地失败")
            return False
            
        # 选择出发时间（如果提供）
        if departure_time and not self.select_departure_time(departure_time):
            self.logger.error("选择出发时间失败")
            return False
            
        # 点击搜索
        if not self.click_search_button():
            self.logger.error("点击搜索按钮失败")
            return False
            
        # 等待加载完成
        self.wait_for_loading_complete()
        
        return True
        
    def get_trip_count(self):
        """
        获取搜索结果数量
        
        Returns:
            int: 行程数量
        """
        try:
            trip_elements = self.driver.find_elements(*self.TRIP_ITEM)
            return len(trip_elements)
        except Exception:
            return 0
            
    def is_empty_result(self):
        """
        检查是否为空结果
        
        Returns:
            bool: 是否为空结果
        """
        return self.is_element_visible(self.EMPTY_STATE)
        
    def book_first_trip(self):
        """
        预订第一个行程
        
        Returns:
            bool: 是否预订成功
        """
        try:
            trip_items = self.driver.find_elements(*self.TRIP_ITEM)
            if not trip_items:
                self.logger.error("没有找到行程项目")
                return False
                
            # 点击第一个行程的预订按钮
            book_btn = trip_items[0].find_element(By.CSS_SELECTOR, ".book-btn, .book")
            book_btn.click()
            
            # 等待页面跳转或弹窗
            time.sleep(2)
            return True
            
        except Exception as e:
            self.logger.error(f"预订行程失败: {e}")
            return False


class PublishTripPage(BasePage):
    """发布行程页面"""
    
    # 表单元素
    START_LOCATION_INPUT = (By.CSS_SELECTOR, "input[placeholder*='出发地'], .start-location input")
    END_LOCATION_INPUT = (By.CSS_SELECTOR, "input[placeholder*='目的地'], .end-location input")
    DEPARTURE_TIME_PICKER = (By.CSS_SELECTOR, "picker[class*='time'], .time-picker")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='价格'], .price-input input")
    SEAT_COUNT_INPUT = (By.CSS_SELECTOR, "input[placeholder*='座位'], .seat-input input")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[placeholder*='描述'], .description textarea")
    
    # 车辆选择
    CAR_SELECT = (By.CSS_SELECTOR, "picker[class*='car'], .car-picker")
    
    # 按钮
    PUBLISH_BUTTON = (By.CSS_SELECTOR, "button[class*='publish'], .publish-btn")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button[class*='cancel'], .cancel-btn")
    
    def __init__(self, driver_manager):
        """初始化发布行程页面"""
        super().__init__(driver_manager)
        
    def navigate_to_publish_trip(self):
        """导航到发布行程页面"""
        self.navigate_to_page(PageConfig.PAGES["publish_trip"])
        
    def input_start_location(self, location):
        """输入出发地"""
        return self.input_text(self.START_LOCATION_INPUT, location)
        
    def input_end_location(self, location):
        """输入目的地"""
        return self.input_text(self.END_LOCATION_INPUT, location)
        
    def input_price(self, price):
        """输入价格"""
        return self.input_text(self.PRICE_INPUT, str(price))
        
    def input_seat_count(self, seat_count):
        """输入座位数"""
        return self.input_text(self.SEAT_COUNT_INPUT, str(seat_count))
        
    def input_description(self, description):
        """输入描述"""
        return self.input_text(self.DESCRIPTION_INPUT, description)
        
    def select_departure_time(self, time_str):
        """选择出发时间"""
        try:
            if not self.click_element(self.DEPARTURE_TIME_PICKER):
                return False
            time.sleep(1)
            # 确认选择
            confirm_btn = (By.CSS_SELECTOR, ".picker-confirm, .confirm-btn")
            return self.click_element(confirm_btn)
        except Exception as e:
            self.logger.error(f"选择出发时间失败: {e}")
            return False
            
    def select_car(self):
        """选择车辆"""
        try:
            if not self.click_element(self.CAR_SELECT):
                return False
            time.sleep(1)
            # 选择第一个车辆
            first_car = (By.CSS_SELECTOR, ".car-option:first-child, .picker-item:first-child")
            self.click_element(first_car)
            # 确认选择
            confirm_btn = (By.CSS_SELECTOR, ".picker-confirm, .confirm-btn")
            return self.click_element(confirm_btn)
        except Exception as e:
            self.logger.error(f"选择车辆失败: {e}")
            return False
            
    def click_publish_button(self):
        """点击发布按钮"""
        return self.click_element(self.PUBLISH_BUTTON)
        
    def publish_trip(self, trip_data):
        """
        发布行程
        
        Args:
            trip_data (dict): 行程数据
            
        Returns:
            bool: 是否发布成功
        """
        self.logger.info(f"发布行程：{trip_data.get('startLocation')} -> {trip_data.get('endLocation')}")
        
        # 输入出发地
        if not self.input_start_location(trip_data.get('startLocation', '')):
            self.logger.error("输入出发地失败")
            return False
            
        # 输入目的地
        if not self.input_end_location(trip_data.get('endLocation', '')):
            self.logger.error("输入目的地失败")
            return False
            
        # 选择出发时间
        if not self.select_departure_time(trip_data.get('departureTime', '')):
            self.logger.error("选择出发时间失败")
            return False
            
        # 输入价格
        if not self.input_price(trip_data.get('price', '')):
            self.logger.error("输入价格失败")
            return False
            
        # 输入座位数
        if not self.input_seat_count(trip_data.get('seatAvailable', '')):
            self.logger.error("输入座位数失败")
            return False
            
        # 输入描述
        if not self.input_description(trip_data.get('description', '')):
            self.logger.error("输入描述失败")
            return False
            
        # 选择车辆
        if not self.select_car():
            self.logger.error("选择车辆失败")
            return False
            
        # 记录当前URL
        current_url = self.get_current_url()
        
        # 点击发布按钮
        if not self.click_publish_button():
            self.logger.error("点击发布按钮失败")
            return False
            
        # 等待加载完成
        self.wait_for_loading_complete()
        
        # 检查是否发布成功
        if self.wait_for_page_change(current_url, timeout=10):
            self.logger.info("行程发布成功")
            return True
        else:
            error_msg = self.wait_for_toast_message()
            self.logger.error(f"行程发布失败: {error_msg}")
            return False
            
    def is_publish_page_loaded(self):
        """检查发布页面是否加载完成"""
        return (self.is_element_visible(self.START_LOCATION_INPUT) and 
                self.is_element_visible(self.END_LOCATION_INPUT) and 
                self.is_element_visible(self.PUBLISH_BUTTON))