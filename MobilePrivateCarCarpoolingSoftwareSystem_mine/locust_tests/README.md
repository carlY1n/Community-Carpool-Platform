# 拼车系统性能测试项目

基于Locust框架的拼车系统性能测试项目，提供全面的API性能测试和负载测试功能。

## 🚀 项目特性

- **多场景测试**: 支持轻负载、正常负载、高负载、压力测试、峰值测试、稳定性测试
- **模块化设计**: 分别测试认证、行程、预订等核心模块
- **真实用户行为**: 模拟乘客、司机、管理员等不同角色的操作
- **丰富的报告**: HTML、CSV、JSON格式的详细测试报告
- **数据生成**: 自动生成测试数据，支持批量用户和行程创建
- **性能监控**: 实时监控响应时间、错误率、RPS等关键指标
- **阈值检查**: 自动检查性能指标是否满足预设阈值

## 📁 项目结构

```
locust_tests/
├── locustfile.py              # 主测试文件
├── config.py                  # 配置文件
├── run_tests.py              # 测试运行脚本
├── requirements.txt          # 依赖包列表
├── README.md                 # 项目说明
├── scenarios/                # 测试场景
│   ├── auth_scenario.py      # 认证测试场景
│   ├── trip_scenario.py      # 行程测试场景
│   └── booking_scenario.py   # 预订测试场景
├── utils/                    # 工具模块
│   ├── data_generator.py     # 测试数据生成器
│   └── report_generator.py   # 报告生成器
├── reports/                  # 测试报告目录
└── logs/                     # 日志目录
```

## 🛠️ 环境准备

### 1. Python环境
确保Python版本 >= 3.7

### 2. 安装依赖
```bash
cd locust_tests
pip install -r requirements.txt
```

### 3. 系统要求
- 拼车系统后端服务运行在 `http://localhost:8888`
- 确保数据库连接正常
- 建议系统内存 >= 4GB

## 🎯 快速开始

### 1. 基础测试
```bash
# 运行默认的正常负载测试
python run_tests.py

# 指定测试场景
python run_tests.py --scenario light    # 轻负载
python run_tests.py --scenario high     # 高负载
python run_tests.py --scenario stress   # 压力测试
```

### 2. 自定义参数
```bash
# 自定义用户数和运行时间
python run_tests.py --users 100 --spawn-rate 5 --run-time 10m

# 指定目标主机
python run_tests.py --host http://192.168.1.100:8888
```

### 3. 模块测试
```bash
# 仅测试认证模块
python run_tests.py --auth-only

# 仅测试行程模块
python run_tests.py --trip-only

# 仅测试预订模块
python run_tests.py --booking-only

# 运行所有模块测试
python run_tests.py --all-modules
```

### 4. Web UI模式
```bash
# 启动Web界面
python run_tests.py --web-ui

# 自定义端口
python run_tests.py --web-ui --port 8090
```

## 📊 测试场景说明

### 轻负载测试 (light)
- **用户数**: 10
- **启动速率**: 1用户/秒
- **运行时间**: 2分钟
- **用途**: 验证基本功能

### 正常负载测试 (normal)
- **用户数**: 50
- **启动速率**: 2用户/秒
- **运行时间**: 5分钟
- **用途**: 模拟日常使用场景

### 高负载测试 (high)
- **用户数**: 100
- **启动速率**: 5用户/秒
- **运行时间**: 10分钟
- **用途**: 模拟高峰期使用

### 压力测试 (stress)
- **用户数**: 200
- **启动速率**: 10用户/秒
- **运行时间**: 15分钟
- **用途**: 测试系统极限

### 峰值测试 (spike)
- **用户数**: 500
- **启动速率**: 50用户/秒
- **运行时间**: 3分钟
- **用途**: 测试突发流量处理

### 稳定性测试 (stability)
- **用户数**: 30
- **启动速率**: 1用户/秒
- **运行时间**: 30分钟
- **用途**: 长时间稳定性验证

## 🧪 测试用户角色

### 乘客用户 (PassengerUser)
- 搜索行程 (权重: 5)
- 查看行程详情 (权重: 3)
- 预订行程 (权重: 2)
- 查看我的预订 (权重: 2)
- 取消预订 (权重: 1)

### 司机用户 (DriverUser)
- 发布行程 (权重: 4)
- 查看我的行程 (权重: 3)
- 管理预订 (权重: 2)
- 确认预订 (权重: 2)
- 取消行程 (权重: 1)

### 管理员用户 (AdminUser)
- 查看所有用户 (权重: 3)
- 查看所有行程 (权重: 2)
- 查看所有预订 (权重: 2)
- 查看投诉 (权重: 1)

## 📈 性能指标

### 关键指标
- **响应时间**: 平均响应时间 < 500ms
- **95%响应时间**: < 2000ms
- **错误率**: < 5%
- **RPS**: > 10请求/秒

### 监控内容
- API响应时间分布
- 错误类型和频率
- 系统吞吐量
- 并发用户处理能力

## 📋 测试报告

### HTML报告
- 包含详细的性能统计
- 可视化图表展示
- 性能阈值检查结果
- 优化建议

### CSV报告
- 原始统计数据
- 便于进一步分析
- 支持Excel打开

### JSON报告
- 结构化数据
- 便于程序处理
- 支持CI/CD集成

## 🔧 配置说明

### 环境变量
```bash
# 设置目标主机
export LOCUST_HOST=http://localhost:8888

# 设置并发用户数
export LOCUST_USERS=50

# 设置运行时间
export LOCUST_RUN_TIME=5m

# 启用无头模式
export LOCUST_HEADLESS=true
```

### 配置文件
编辑 `config.py` 文件可以修改：
- 测试用户数据
- API端点配置
- 性能阈值设置
- 报告配置

## 🚨 注意事项

### 测试前准备
1. 确保后端服务正常运行
2. 数据库中有足够的测试数据
3. 检查网络连接稳定性
4. 关闭不必要的应用程序

### 测试数据
- 使用预设的测试用户账号
- 自动生成随机测试数据
- 避免使用生产环境数据

### 性能影响
- 高负载测试可能影响系统性能
- 建议在测试环境中运行
- 监控系统资源使用情况

## 🔍 故障排除

### 常见问题

#### 1. 连接错误
```
ConnectionError: HTTPConnectionPool
```
**解决方案**: 检查后端服务是否启动，确认主机地址正确

#### 2. 认证失败
```
401 Unauthorized
```
**解决方案**: 检查测试用户账号是否存在，密码是否正确

#### 3. 依赖包错误
```
ModuleNotFoundError: No module named 'locust'
```
**解决方案**: 运行 `pip install -r requirements.txt`

#### 4. 内存不足
```
MemoryError
```
**解决方案**: 减少并发用户数，增加系统内存

### 调试模式
```bash
# 启用详细日志
python run_tests.py --loglevel DEBUG

# 单用户测试
python run_tests.py --users 1 --run-time 30s
```

## 📞 技术支持

### 日志查看
- 测试日志保存在 `logs/` 目录
- 使用 `--loglevel DEBUG` 获取详细信息

### 性能调优
- 根据测试报告中的建议进行优化
- 关注响应时间最长的API
- 检查错误率较高的接口

### 扩展开发
- 在 `scenarios/` 目录添加新的测试场景
- 修改 `utils/data_generator.py` 生成特定测试数据
- 自定义 `utils/report_generator.py` 报告格式

## 📝 更新日志

### v1.0.0 (2024-01-15)
- 初始版本发布
- 支持基础性能测试功能
- 包含认证、行程、预订模块测试
- 提供多种测试场景和报告格式

---

**拼车系统性能测试项目** - 基于Locust的专业性能测试解决方案 