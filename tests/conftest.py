import asyncio
import os
from datetime import datetime
from typing import Any, Dict, Generator, List

import allure
import pytest
from loguru import logger
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

# 配置loguru日志
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logger.add(log_file, rotation="10 MB", retention="7 days", level="INFO")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """创建事件循环，用于异步测试"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def playwright() -> Generator[Any, None, None]:
    """创建Playwright实例"""
    async with async_playwright() as playwright_instance:
        yield playwright_instance


@pytest.fixture(scope="session")
async def browser_type(playwright) -> str:
    """获取浏览器类型"""
    # 从配置文件读取浏览器类型
    import yaml
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "env.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    browser_type = config.get("browser", {}).get("type", "chromium")
    return browser_type


@pytest.fixture(scope="session")
async def browser(playwright, browser_type) -> Generator[Browser, None, None]:
    """创建浏览器实例"""
    # 从配置文件读取浏览器配置
    import yaml
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "env.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    browser_config = config.get("browser", {})
    headless = browser_config.get("headless", False)
    slow_mo = browser_config.get("slow_mo", 50)
    
    # 启动浏览器
    if browser_type == "chromium":
        browser_instance = await playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    elif browser_type == "firefox":
        browser_instance = await playwright.firefox.launch(headless=headless, slow_mo=slow_mo)
    elif browser_type == "webkit":
        browser_instance = await playwright.webkit.launch(headless=headless, slow_mo=slow_mo)
    else:
        browser_instance = await playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    
    logger.info(f"启动浏览器: {browser_type}, headless={headless}, slow_mo={slow_mo}ms")
    yield browser_instance
    await browser_instance.close()
    logger.info("关闭浏览器")


@pytest.fixture(scope="function")
async def context(browser) -> Generator[BrowserContext, None, None]:
    """创建浏览器上下文"""
    context_instance = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "videos")
    )
    
    # 启用请求和响应记录
    await context_instance.route("**/*", lambda route: route.continue_())
    
    logger.info("创建浏览器上下文")
    yield context_instance
    await context_instance.close()
    logger.info("关闭浏览器上下文")


@pytest.fixture(scope="function")
async def page(context) -> Generator[Page, None, None]:
    """创建页面实例"""
    page_instance = await context.new_page()
    
    # 监听控制台日志
    page_instance.on("console", lambda msg: logger.debug(f"浏览器控制台: {msg.text}"))
    
    # 监听页面错误
    page_instance.on("pageerror", lambda err: logger.error(f"页面错误: {err}"))
    
    # 监听请求
    page_instance.on("request", lambda request: logger.debug(f"请求: {request.method} {request.url}"))
    
    # 监听响应
    page_instance.on("response", lambda response: logger.debug(f"响应: {response.status} {response.url}"))
    
    logger.info("创建新页面")
    yield page_instance
    logger.info("关闭页面")


@pytest.fixture(scope="function")
def test_result_csv():
    """创建测试结果CSV文件"""
    import csv
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, f"test_result_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["用例ID", "执行状态", "耗时(秒)", "失败原因", "截图路径"])
    
    logger.info(f"创建测试结果文件: {csv_path}")
    return csv_path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试结果钩子，用于在测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    
    # 测试失败时自动截图
    if report.when == "call" and report.failed:
        try:
            # 如果测试用例使用了page夹具，则截图
            if "page" in item.funcargs:
                page = item.funcargs["page"]
                screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                
                # 同步截图
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(page.screenshot(path=screenshot_path))
                else:
                    loop.run_until_complete(page.screenshot(path=screenshot_path))
                
                # 添加截图到Allure报告
                allure.attach.file(screenshot_path, name="失败截图", attachment_type=allure.attachment_type.PNG)
                
                logger.info(f"测试失败截图: {screenshot_path}")
                
                # 更新测试结果CSV
                if "test_result_csv" in item.funcargs:
                    csv_path = item.funcargs["test_result_csv"]
                    with open(csv_path, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            item.name,
                            "失败",
                            report.duration,
                            str(report.longrepr),
                            screenshot_path
                        ])
        except Exception as e:
            logger.error(f"测试失败截图异常: {e}")
    
    # 测试成功时更新CSV
    elif report.when == "call" and report.passed:
        try:
            if "test_result_csv" in item.funcargs:
                csv_path = item.funcargs["test_result_csv"]
                with open(csv_path, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        item.name,
                        "成功",
                        report.duration,
                        "",
                        ""
                    ])
        except Exception as e:
            logger.error(f"更新测试结果CSV异常: {e}")