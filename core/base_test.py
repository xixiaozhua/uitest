import allure
import pytest_asyncio
from playwright.async_api import async_playwright, Page, Browser
from utils.file_read import read_yaml
from typing import Dict, Any

class BaseTest:
    """测试基类（仅保留业务逻辑）"""
    
    async def get_config(self, env: str) -> dict:
        return read_yaml('config/env.yaml', env=env)

    async def goto(self, page: Page, env: str, path: str = ""):
        """整合导航与异常处理"""
        config = await self.get_config(env)
        base_url = config['base_url'].rstrip('/')
        target_url = f"{base_url}/{path.lstrip('/')}" if path else base_url
        
        try:
            await page.goto(target_url, timeout=config['timeout'])
        except Exception as e:
            await self._capture_failure(page, f"导航失败: {str(e)}")
            raise

    async def _capture_failure(self, page: Page, message: str):
        """统一失败处理"""
        await self.take_screenshot(page, "操作失败截图")
        allure.dynamic.description(message)

    @pytest_asyncio.fixture(scope="function")
    async def browser(self, env: str) -> Browser:
        """浏览器实例fixture"""
        config = await self.get_config(env)
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=config['headless'],
            timeout=config['timeout']
        )
        yield browser
        await browser.close()
        await playwright.stop()

    @pytest_asyncio.fixture(scope="function")
    async def page(self, browser: Browser) -> Page:
        """页面实例fixture"""
        return await browser.new_page()

    @pytest_asyncio.fixture(autouse=True)
    async def auto_teardown(self, request, page: Page) -> None:
        """带失败检测的自动清理"""
        yield
        # 仅在测试失败时截图
        if request.node.rep_call.failed:
            await self.take_screenshot(page, "测试失败截图")
        # 无论成功失败都关闭页面
        await page.close()

    async def take_screenshot(self, page: Page, name: str) -> None:
        """增强版截图方法"""
        screenshot = await page.screenshot(full_page=True, type="png")
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )