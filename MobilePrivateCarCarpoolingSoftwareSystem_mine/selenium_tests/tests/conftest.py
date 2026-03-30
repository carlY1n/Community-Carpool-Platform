"""
pytest配置文件和公共fixtures
"""
import pytest
import logging
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.trip_page import SearchTripPage, PublishTripPage
from config.config import TestConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope="session")
def driver_manager():
    """会话级别的driver管理器fixture"""
    dm = DriverManager()
    dm.create_driver(headless=False, mobile_emulation=True)
    yield dm
    dm.quit_driver()

@pytest.fixture(scope="function")
def fresh_driver():
    """函数级别的独立driver fixture"""
    dm = DriverManager()
    dm.create_driver(headless=False, mobile_emulation=True)
    yield dm
    dm.quit_driver()

@pytest.fixture
def login_page(driver_manager):
    """登录页面fixture"""
    return LoginPage(driver_manager)

@pytest.fixture
def register_page(driver_manager):
    """注册页面fixture"""
    return RegisterPage(driver_manager)

@pytest.fixture
def search_trip_page(driver_manager):
    """搜索行程页面fixture"""
    return SearchTripPage(driver_manager)

@pytest.fixture
def publish_trip_page(driver_manager):
    """发布行程页面fixture"""
    return PublishTripPage(driver_manager)

@pytest.fixture
def test_passenger_user():
    """测试乘客用户数据fixture"""
    return TestConfig.TEST_USERS["passenger"].copy()

@pytest.fixture
def test_driver_user():
    """测试司机用户数据fixture"""
    return TestConfig.TEST_USERS["driver"].copy()

@pytest.fixture
def test_admin_user():
    """测试管理员用户数据fixture"""
    return TestConfig.TEST_USERS["admin"].copy()

@pytest.fixture
def test_trip_data():
    """测试行程数据fixture"""
    return TestConfig.TEST_TRIP_DATA.copy()

@pytest.fixture(autouse=True)
def setup_and_teardown(driver_manager):
    """每个测试的设置和清理"""
    # 测试前设置
    driver = driver_manager.get_driver()
    driver.delete_all_cookies()  # 清除cookies
    
    yield
    
    # 测试后清理
    try:
        # 截图保存（如果测试失败）
        test_name = os.environ.get('PYTEST_CURRENT_TEST', 'unknown').split(' ')[0]
        screenshot_path = driver_manager.take_screenshot(f"{test_name}_teardown.png")
        if screenshot_path:
            print(f"测试结束截图: {screenshot_path}")
    except Exception as e:
        print(f"清理时出错: {e}")

@pytest.fixture
def logged_in_passenger(driver_manager, login_page, test_passenger_user):
    """已登录的乘客用户fixture"""
    login_page.navigate_to_login()
    success = login_page.login(
        test_passenger_user["phone"], 
        test_passenger_user["password"]
    )
    if not success:
        pytest.skip("登录失败，跳过测试")
    return test_passenger_user

@pytest.fixture
def logged_in_driver(driver_manager, login_page, test_driver_user):
    """已登录的司机用户fixture"""
    login_page.navigate_to_login()
    success = login_page.login(
        test_driver_user["phone"], 
        test_driver_user["password"]
    )
    if not success:
        pytest.skip("登录失败，跳过测试")
    return test_driver_user

# pytest hooks
def pytest_configure(config):
    """pytest配置钩子"""
    # 确保必要的目录存在
    os.makedirs(TestConfig.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(TestConfig.REPORT_DIR, exist_ok=True)

def pytest_runtest_makereport(item, call):
    """生成测试报告钩子"""
    if call.when == "call" and call.excinfo is not None:
        # 测试失败时进行截图
        try:
            driver_manager = item.funcargs.get('driver_manager')
            if driver_manager:
                screenshot_path = driver_manager.take_screenshot(f"{item.name}_failed.png")
                if screenshot_path:
                    print(f"测试失败截图: {screenshot_path}")
        except Exception as e:
            print(f"失败截图时出错: {e}")

# 命令行选项
def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False,
        help="运行无头模式"
    )
    parser.addoption(
        "--base-url", 
        action="store", 
        default=TestConfig.BASE_URL,
        help="测试基础URL"
    )
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="浏览器类型"
    )

@pytest.fixture(scope="session")
def test_config(request):
    """测试配置参数fixture"""
    return {
        "headless": request.config.getoption("--headless"),
        "base_url": request.config.getoption("--base-url"),
        "browser": request.config.getoption("--browser")
    }

# 测试标记定义
# 这些标记在pytest.ini中已定义，这里只是注释说明
# smoke: 冒烟测试，核心功能快速验证
# critical: 关键功能测试，主要业务流程
# regression: 回归测试，边界和异常情况
# integration: 集成测试，多模块协同
# performance: 性能测试，响应时间验证 