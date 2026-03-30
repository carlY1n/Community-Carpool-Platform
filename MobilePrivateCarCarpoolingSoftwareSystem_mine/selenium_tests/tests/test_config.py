"""
配置验证测试
"""
import pytest
from config.config import TestConfig, PageConfig

class TestConfiguration:
    """配置测试类"""
    
    @pytest.mark.smoke
    def test_config_values(self):
        """测试配置值是否正确"""
        assert TestConfig.BASE_URL == "http://localhost:8080"
        assert TestConfig.API_BASE_URL == "http://localhost:8888"
        assert TestConfig.IMPLICIT_WAIT == 10
        assert TestConfig.EXPLICIT_WAIT == 20
        
    @pytest.mark.smoke
    def test_test_users_config(self):
        """测试用户配置"""
        assert "passenger" in TestConfig.TEST_USERS
        assert "driver" in TestConfig.TEST_USERS
        assert "admin" in TestConfig.TEST_USERS
        
        passenger = TestConfig.TEST_USERS["passenger"]
        assert "phone" in passenger
        assert "password" in passenger
        assert "userType" in passenger
        
    @pytest.mark.smoke
    def test_page_config(self):
        """测试页面配置"""
        assert "login" in PageConfig.PAGES
        assert "register" in PageConfig.PAGES
        assert "search_trip" in PageConfig.PAGES
        assert "publish_trip" in PageConfig.PAGES
        
    @pytest.mark.smoke
    def test_chromedriver_paths(self):
        """测试ChromeDriver路径配置"""
        paths = TestConfig.get_chromedriver_paths()
        assert isinstance(paths, list)
        assert len(paths) > 0 