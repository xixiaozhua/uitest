import allure
import pytest_asyncio
from playwright.async_api import async_playwright
from utils.file_read import read_yaml
from playwright.async_api import Page

class BaseTest:
    """测试基类，封装通用测试功能"""
    
    async def get_config(self, env: str) -> dict:
        """获取指定环境配置"""
        return read_yaml('config/env.yaml', env=env)
    
    @pytest_asyncio.fixture(scope="function")
    async def browser(self, env: str):
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
    async def page(self, browser):
        """页面实例fixture"""
        return await browser.new_page()

    async def goto(self, page: Page, env: str, path: str = ""):
        """导航到指定页面"""
        config = await self.get_config(env)
        base_url = config['base_url'].rstrip('/')
        target_url = f"{base_url}/{path.lstrip('/')}" if path else base_url
        await page.goto(target_url, timeout=config['timeout'])
    
    async def take_screenshot(self, page, name: str):
        """截取页面截图并附加到Allure报告"""
        screenshot = await page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    
    async def teardown_method(self, page):
        """测试清理方法"""
        await self.take_screenshot(page, "测试结束截图")
        await page.close()