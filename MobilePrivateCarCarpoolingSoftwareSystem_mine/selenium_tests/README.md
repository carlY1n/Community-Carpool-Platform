# 拼车系统Selenium功能测试

基于Selenium + ChromeDriver的拼车系统前端功能测试自动化项目。

## 项目概述

本项目针对移动端私家车拼车软件系统(UniApp H5)进行功能测试，覆盖用户注册登录、行程管理、订单处理等核心业务流程。

## 技术栈

- **测试框架**: pytest
- **UI自动化**: Selenium WebDriver
- **浏览器**: Chrome + ChromeDriver (自动管理)
- **报告**: pytest-html, Allure
- **语言**: Python 3.7+

## 项目结构

```
selenium_tests/
├── config/                 # 配置文件
│   └── config.py           # 测试配置
├── pages/                  # 页面对象模型
│   ├── base_page.py        # 页面基类
│   ├── login_page.py       # 登录页面
│   ├── register_page.py    # 注册页面
│   └── trip_page.py        # 行程页面
├── tests/                  # 测试用例
│   ├── conftest.py         # pytest配置
│   ├── test_user_auth.py   # 用户认证测试
│   └── test_trip_management.py # 行程管理测试
├── utils/                  # 工具类
│   └── driver_manager.py   # WebDriver管理器
├── screenshots/            # 截图目录
├── reports/               # 测试报告目录
├── requirements.txt       # 依赖列表
├── run_tests.py          # 测试运行脚本
└── README.md             # 项目说明
```

## 环境要求

- Python 3.7+
- Chrome浏览器 (最新版本)
- 网络连接 (用于下载ChromeDriver)

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置ChromeDriver

如果您有本地的ChromeDriver文件（如chromedriver-win64文件夹），可以使用以下方式配置：

#### 方式一：使用设置脚本（推荐）
```bash
python setup_chromedriver.py
```

#### 方式二：手动配置
将`chromedriver-win64`文件夹放在以下任一位置：
- 项目根目录（与selenium_tests同级）
- selenium_tests目录内
- 或直接将chromedriver.exe放在selenium_tests目录

项目会自动搜索以下路径：
- `../chromedriver-win64/chromedriver.exe`
- `chromedriver-win64/chromedriver.exe`
- `./chromedriver-win64/chromedriver.exe`
- `chromedriver.exe`

如果找不到本地ChromeDriver，系统会自动下载最新版本。

### 3. 启动前端应用

确保拼车系统前端应用运行在 `http://localhost:8080`

### 4. 启动后端服务

确保后端API服务运行在 `http://localhost:8888`

### 5. 运行测试

#### 运行所有测试
```bash
python run_tests.py
```

#### 运行特定标记的测试
```bash
# 冒烟测试
python run_tests.py -m smoke

# 关键功能测试
python run_tests.py -m critical

# 回归测试
python run_tests.py -m regression
```

#### 生成HTML报告
```bash
python run_tests.py --html-report
```

#### 无头模式运行
```bash
python run_tests.py --headless
```

#### 并行执行
```bash
python run_tests.py -n 4
```

## 测试用例分类

### 用户认证测试 (`test_user_auth.py`)

- ✅ 登录页面加载
- ✅ 注册页面加载
- ✅ 有效用户登录
- ✅ 无效密码登录
- ✅ 无效手机号登录
- ✅ 空字段登录
- ✅ 乘客注册
- ✅ 司机注册
- ✅ 重复手机号注册
- ✅ 无效手机号格式注册
- ✅ 无效身份证号注册
- ✅ 必填字段为空注册
- ✅ 注册后立即登录
- ✅ 登录注册页面间导航

### 行程管理测试 (`test_trip_management.py`)

- ✅ 搜索行程页面加载
- ✅ 发布行程页面加载
- ✅ 基本行程搜索
- ✅ 带时间的行程搜索
- ✅ 完整的行程发布流程
- ✅ 发布行程缺少必填字段
- ✅ 发布行程无效价格
- ✅ 发布行程无效座位数
- ✅ 搜索并预订行程流程
- ✅ 搜索空地点
- ✅ 搜索相同起终点
- ✅ 搜索不存在地点
- ✅ 连续多次搜索
- ✅ 搜索响应时间测试
- ✅ 发布后搜索自己的行程

## 测试标记

- `@pytest.mark.smoke` - 冒烟测试，核心功能快速验证
- `@pytest.mark.critical` - 关键功能测试，主要业务流程
- `@pytest.mark.regression` - 回归测试，边界和异常情况
- `@pytest.mark.integration` - 集成测试，多模块协同
- `@pytest.mark.performance` - 性能测试，响应时间验证

## 配置说明

### 环境配置 (`config/config.py`)

```python
# 测试环境URL
BASE_URL = "http://localhost:8080"
API_BASE_URL = "http://localhost:8888"

# 测试用户数据
TEST_USERS = {
    "passenger": {...},
    "driver": {...},
    "admin": {...}
}

# Chrome浏览器选项
CHROME_OPTIONS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--window-size=1920,1080"
]
```

### 移动端模拟

项目默认启用移动端模拟，模拟iPhone设备访问UniApp H5页面：

```python
mobile_emulation_config = {
    "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) ..."
}
```

## 高级功能

### 截图功能

- 测试失败时自动截图
- 手动截图：`driver_manager.take_screenshot("filename.png")`
- 截图保存在 `screenshots/` 目录

### 测试报告

#### HTML报告
```bash
python run_tests.py --html-report
```
报告保存在 `reports/test_report_YYYYMMDD_HHMMSS.html`

#### Allure报告
```bash
python run_tests.py --allure
```
报告数据保存在 `reports/allure-results/`

### 并行执行

使用pytest-xdist实现并行执行：
```bash
python run_tests.py -n 4  # 4个进程并行
```

### 等待策略

项目实现了多种等待策略：
- 隐式等待：默认10秒
- 显式等待：针对特定元素
- 页面加载等待：确保UniApp渲染完成

## 页面对象模型

### BasePage

所有页面类的基类，提供通用方法：
- `navigate_to_page(page_path)` - 页面导航
- `wait_for_toast_message()` - 等待toast消息
- `is_element_present()` - 检查元素存在
- `click_element()` - 安全点击
- `input_text()` - 安全输入

### LoginPage

登录页面操作：
- `login(phone, password)` - 执行登录
- `get_error_message()` - 获取错误消息

### RegisterPage

注册页面操作：
- `register(user_data)` - 执行注册
- `select_user_type()` - 选择用户类型

### TripPage

行程相关页面：
- `SearchTripPage` - 搜索行程
- `PublishTripPage` - 发布行程

## 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   - 项目优先使用本地ChromeDriver，如果版本不匹配可运行 `python setup_chromedriver.py` 重新配置
   - 或删除本地ChromeDriver让系统自动下载最新版本

2. **元素定位失败**
   - 检查页面是否完全加载
   - 验证元素选择器是否正确
   - 确认移动端模拟是否正常

3. **测试超时**
   - 检查网络连接
   - 增加等待时间配置
   - 确认前后端服务正常运行

4. **页面跳转失败**
   - 确认路由配置正确
   - 检查UniApp H5路由模式

### 调试技巧

1. **禁用无头模式**
   ```bash
   python run_tests.py  # 默认有头模式，可观察浏览器行为
   ```

2. **增加详细日志**
   ```bash
   python run_tests.py -v
   ```

3. **运行单个测试**
   ```bash
   python run_tests.py -t tests/test_user_auth.py::TestUserAuth::test_valid_login
   ```

4. **保留浏览器窗口**
   在代码中添加断点或sleep，观察页面状态

## 扩展开发

### 添加新页面

1. 在 `pages/` 目录创建页面类
2. 继承 `BasePage`
3. 定义页面元素定位器
4. 实现页面操作方法

### 添加新测试

1. 在 `tests/` 目录创建测试文件
2. 使用合适的pytest标记
3. 添加fixture依赖
4. 编写测试断言

### 集成CI/CD

```yaml
# GitHub Actions示例
- name: Run Selenium Tests
  run: |
    python run_tests.py --headless --html-report
```

## 最佳实践

1. **页面对象模型** - 将页面操作封装在页面类中
2. **等待策略** - 使用显式等待而非固定sleep
3. **数据驱动** - 使用pytest参数化进行数据驱动测试
4. **失败重试** - 针对不稳定的测试添加重试机制
5. **环境隔离** - 使用独立的测试数据和环境

## 维护指南

1. **定期更新依赖** - 保持Selenium和pytest最新版本
2. **元素定位维护** - 页面改动时更新选择器
3. **测试数据管理** - 定期清理和更新测试数据
4. **性能监控** - 关注测试执行时间和成功率

## 许可证

本项目仅用于拼车系统的功能测试，不得用于其他商业用途。 