# UI自动化测试框架

基于Playwright和Pytest的现代化UI自动化测试框架，支持异步测试、数据驱动和多浏览器测试。

## 技术栈

- Python 3.10+ (支持async/await语法)
- Playwright 1.40+ (内置Chromium浏览器)
- pytest 8.0+ (测试用例管理框架)
- Allure 2.13+ (测试报告生成)
- Loguru 0.7+ (结构化日志记录)
- pytest-asyncio (异步测试支持)
- pytest-xdist (并行测试执行)

## 框架特性

- **异步测试支持**：所有操作使用Playwright异步API
- **数据驱动测试**：支持CSV/YAML文件参数化
- **企业级特性**：
  - 使用相对路径
  - 多浏览器支持（Chromium/Firefox/WebKit）
  - 自动化等待机制（网络空闲检测+元素稳定判定）
- **自动化截图**：测试失败时自动截图
- **详细日志**：记录关键操作、元素定位轨迹和性能指标
- **性能监控**：记录页面加载时间和API响应时长

## 项目结构

```
/uitest
├── config
│   └── env.yaml        # 环境变量
├── pages
│   ├── base_page.py    # 页面对象基类
│   └── login_page.py   # 登录页面对象
├── tests
│   ├── conftest.py     # pytest全局夹具
│   └── test_login.py   # 登录页面测试
├── utils
│   └── file_read.py    # 文件读取工具
├── output
│   ├── logs/           # 日志文件
│   ├── screenshots/    # 截图文件
│   └── videos/         # 视频录制
└── data
    └── login_cases.csv # 登录测试数据集
```

## 安装依赖

```bash
# 安装Python依赖
pip install playwright pytest pytest-asyncio pytest-xdist allure-pytest loguru pyyaml

# 安装Playwright浏览器
python -m playwright install
```

## 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_login.py

# 并行运行测试
pytest tests/ -n auto

# 生成Allure报告
pytest tests/ --alluredir=./allure-results
allure serve ./allure-results
```

## 测试报告

测试结果将保存在以下位置：
- CSV报告：`output/test_result_<timestamp>.csv`
- 日志文件：`output/logs/test_<timestamp>.log`
- 截图文件：`output/screenshots/`
- Allure报告：`allure-results/`

## 页面对象模式

框架使用页面对象模式（POM）来组织UI元素和操作：

- `BasePage`：提供通用的页面操作方法，如元素查找、点击、输入等
- `LoginPage`：特定页面的实现，包含该页面特有的元素和操作

## 异步测试

所有测试和页面操作都使用异步方式实现，提高测试效率：

```python
@pytest.mark.asyncio
async def test_login(page):
    login_page = LoginPage(page)
    await login_page.navigate_to_login()
    await login_page.login("username", "password")
```

## 元素优先级分布

框架按照业务重要性对元素进行分类：

- 高优先级(Core): 45% - 核心业务功能元素
- 中优先级(Important): 30% - 重要但非核心元素
- 低优先级(Optional): 25% - 可选功能元素

## 自定义配置

通过修改`config/env.yaml`文件可以自定义测试配置：

- 浏览器类型和选项
- 测试环境URL
- 截图和日志设置
- 元素优先级分布
