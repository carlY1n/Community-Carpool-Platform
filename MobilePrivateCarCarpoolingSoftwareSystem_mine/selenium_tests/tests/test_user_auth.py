"""
用户认证功能测试
"""
import pytest
import time
from config.config import TestConfig

class TestUserAuth:
    """用户认证测试类"""
    
    @pytest.mark.smoke
    def test_login_page_load(self, login_page):
        """测试登录页面加载"""
        login_page.navigate_to_login()
        assert login_page.is_login_page_loaded(), "登录页面未正确加载"
        
    @pytest.mark.smoke
    def test_register_page_load(self, register_page):
        """测试注册页面加载"""
        register_page.navigate_to_register()
        assert register_page.is_register_page_loaded(), "注册页面未正确加载"
        
    @pytest.mark.critical
    def test_valid_login(self, login_page, test_passenger_user):
        """测试有效用户登录"""
        login_page.navigate_to_login()
        
        success = login_page.login(
            test_passenger_user["phone"],
            test_passenger_user["password"]
        )
        
        assert success, "登录应该成功"
        
        # 验证登录后的页面变化
        current_url = login_page.get_current_url()
        assert "login" not in current_url, "登录成功后应该跳转离开登录页面"
        
    @pytest.mark.critical
    def test_invalid_login_wrong_password(self, login_page, test_passenger_user):
        """测试错误密码登录"""
        login_page.navigate_to_login()
        
        success = login_page.login(
            test_passenger_user["phone"],
            "wrong_password"
        )
        
        assert not success, "错误密码登录应该失败"
        
        # 检查错误消息
        error_msg = login_page.get_error_message()
        assert error_msg, "应该显示错误消息"
        
    @pytest.mark.critical
    def test_invalid_login_wrong_phone(self, login_page):
        """测试错误手机号登录"""
        login_page.navigate_to_login()
        
        success = login_page.login(
            "19999999999",  # 不存在的手机号
            "123456"
        )
        
        assert not success, "错误手机号登录应该失败"
        
    @pytest.mark.critical
    def test_empty_login_fields(self, login_page):
        """测试空字段登录"""
        login_page.navigate_to_login()
        
        # 测试空手机号
        success = login_page.login("", "123456")
        assert not success, "空手机号登录应该失败"
        
        # 测试空密码
        success = login_page.login("13800138000", "")
        assert not success, "空密码登录应该失败"
        
        # 测试全空
        success = login_page.login("", "")
        assert not success, "全空字段登录应该失败"
        
    @pytest.mark.critical
    def test_valid_passenger_registration(self, register_page):
        """测试乘客注册"""
        register_page.navigate_to_register()
        
        # 使用唯一的测试数据
        unique_phone = f"138{int(time.time()) % 100000000:08d}"
        user_data = {
            "username": f"test_passenger_{int(time.time())}",
            "phone": unique_phone,
            "password": "123456",
            "realName": "测试乘客",
            "idCard": "310101199001011234",
            "userType": "PASSENGER"
        }
        
        success = register_page.register(user_data)
        assert success, "乘客注册应该成功"
        
    @pytest.mark.critical
    def test_valid_driver_registration(self, register_page):
        """测试司机注册"""
        register_page.navigate_to_register()
        
        # 使用唯一的测试数据
        unique_phone = f"139{int(time.time()) % 100000000:08d}"
        user_data = {
            "username": f"test_driver_{int(time.time())}",
            "phone": unique_phone,
            "password": "123456",
            "realName": "测试司机",
            "idCard": "310101199001011235",
            "userType": "DRIVER"
        }
        
        success = register_page.register(user_data)
        assert success, "司机注册应该成功"
        
    @pytest.mark.critical
    def test_duplicate_phone_registration(self, register_page, test_passenger_user):
        """测试重复手机号注册"""
        register_page.navigate_to_register()
        
        # 使用已存在的手机号
        user_data = test_passenger_user.copy()
        user_data["username"] = f"duplicate_user_{int(time.time())}"
        
        success = register_page.register(user_data)
        assert not success, "重复手机号注册应该失败"
        
        # 检查错误消息
        error_msg = register_page.get_error_message()
        assert "已注册" in error_msg or "已存在" in error_msg, "应该提示手机号已注册"
        
    @pytest.mark.regression
    def test_invalid_phone_format_registration(self, register_page):
        """测试无效手机号格式注册"""
        register_page.navigate_to_register()
        
        invalid_phones = [
            "123",  # 太短
            "123456789012345",  # 太长
            "abcdefghijk",  # 非数字
            "12345678901"  # 11位但格式错误
        ]
        
        for phone in invalid_phones:
            user_data = {
                "username": f"test_user_{int(time.time())}",
                "phone": phone,
                "password": "123456",
                "realName": "测试用户",
                "idCard": "310101199001011234",
                "userType": "PASSENGER"
            }
            
            success = register_page.register(user_data)
            assert not success, f"无效手机号 {phone} 注册应该失败"
            
            # 清空表单重新测试
            register_page.clear_all_inputs()
            
    @pytest.mark.regression
    def test_invalid_id_card_registration(self, register_page):
        """测试无效身份证号注册"""
        register_page.navigate_to_register()
        
        invalid_id_cards = [
            "123",  # 太短
            "12345678901234567890",  # 太长
            "abcdefghijklmnopqr",  # 非数字
            "310101199913011234"  # 无效日期
        ]
        
        for id_card in invalid_id_cards:
            unique_phone = f"137{int(time.time()) % 100000000:08d}"
            user_data = {
                "username": f"test_user_{int(time.time())}",
                "phone": unique_phone,
                "password": "123456",
                "realName": "测试用户",
                "idCard": id_card,
                "userType": "PASSENGER"
            }
            
            success = register_page.register(user_data)
            assert not success, f"无效身份证号 {id_card} 注册应该失败"
            
            # 清空表单重新测试
            register_page.clear_all_inputs()
            
    @pytest.mark.regression
    def test_empty_required_fields_registration(self, register_page):
        """测试注册必填字段为空"""
        register_page.navigate_to_register()
        
        # 测试各个必填字段为空的情况
        base_data = {
            "username": "test_user",
            "phone": "13800138999",
            "password": "123456",
            "realName": "测试用户",
            "idCard": "310101199001011234",
            "userType": "PASSENGER"
        }
        
        required_fields = ["username", "phone", "password", "realName", "idCard"]
        
        for field in required_fields:
            test_data = base_data.copy()
            test_data[field] = ""  # 设置为空
            
            success = register_page.register(test_data)
            assert not success, f"必填字段 {field} 为空时注册应该失败"
            
            # 清空表单重新测试
            register_page.clear_all_inputs()
            
    @pytest.mark.integration
    def test_login_after_registration(self, register_page, login_page):
        """测试注册后立即登录"""
        # 注册新用户
        register_page.navigate_to_register()
        
        unique_phone = f"136{int(time.time()) % 100000000:08d}"
        user_data = {
            "username": f"test_reg_login_{int(time.time())}",
            "phone": unique_phone,
            "password": "123456",
            "realName": "测试用户",
            "idCard": "310101199001011234",
            "userType": "PASSENGER"
        }
        
        success = register_page.register(user_data)
        assert success, "注册应该成功"
        
        # 尝试登录
        login_page.navigate_to_login()
        success = login_page.login(user_data["phone"], user_data["password"])
        assert success, "注册后应该能够立即登录"
        
    @pytest.mark.regression
    def test_navigation_between_login_register(self, login_page, register_page):
        """测试登录注册页面间的导航"""
        # 从登录页面到注册页面
        login_page.navigate_to_login()
        login_page.click_register_link()
        
        # 验证跳转到注册页面
        current_url = register_page.get_current_url()
        assert "register" in current_url, "应该跳转到注册页面"
        
        # 从注册页面到登录页面
        register_page.click_login_link()
        
        # 验证跳转到登录页面
        current_url = login_page.get_current_url()
        assert "login" in current_url, "应该跳转到登录页面"