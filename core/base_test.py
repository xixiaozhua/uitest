# -*- coding: utf-8 -*-
"""
测试基类模块
封装测试用例的通用方法和配置
"""

import allure
import pytest_asyncio
from playwright.async_api import async_playwright, Page, Browser
from utils.file_read import read_yaml, read_csv
from typing import Dict, Any, List


class BaseTest:
    """测试基类，封装测试用例的通用方法和配置"""
    
    async def get_config(self, env: str) -> Dict[str, Any]:
        """获取环境配置
        
        Args:
            env: 环境名称
            
        Returns:
            Dict[str, Any]: 环境配置字典
        """
        return read_yaml('config/env.yaml', env=env)
    
    async def get_data(self, file_path: str, has_header: bool = True) -> List[Dict[str, Any]]:
        """读取CSV测试数据
        
        Args:
            file_path: CSV文件路径
            has_header: 是否有表头，默认为True
            
        Returns:
            List[Dict[str, Any]]: 测试数据列表
        """
        return read_csv(f"datas/{file_path}", has_header=has_header)

    async def goto(self, page: Page, env: str, path: str = "") -> None:
        """导航到指定页面
        
        Args:
            page: 页面对象
            env: 环境名称
            path: 目标路径，默认为空
            
        Raises:
            Exception: 页面加载失败时抛出
        """
        try:
            config = await self.get_config(env)
            base_url = config['base_url'].rstrip('/')
            target_url = f"{base_url}/{path.lstrip('/')}" if path else base_url
            
            await page.goto(target_url, timeout=config['timeout'])
            
        except Exception as e:
            await self.take_screenshot(page, "页面加载失败截图")
            raise Exception(f"页面加载失败: {str(e)}")

    async def _capture_failure(self, page: Page, message: str) -> None:
        """统一失败处理
        
        Args:
            page: 页面对象
            message: 失败信息
        """
        await self.take_screenshot(page, "操作失败截图")
        allure.dynamic.description(message)

    @pytest_asyncio.fixture(scope="function")
    async def browser(self, env: str) -> Browser:
        """浏览器实例fixture
        
        Args:
            env: 环境名称
            
        Yields:
            Browser: 浏览器实例
        """
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
        """页面实例fixture
        
        Args:
            browser: 浏览器实例
            
        Returns:
            Page: 页面实例
        """
        return await browser.new_page()

    @pytest_asyncio.fixture(autouse=True)
    async def auto_teardown(self, request, page: Page) -> None:
        """带失败检测的自动清理
        
        Args:
            request: pytest请求对象
            page: 页面对象
        """
        yield
        if request.node.rep_call.failed:
            await self.take_screenshot(page, "测试失败截图")
        await page.close()

    async def take_screenshot(self, page: Page, name: str) -> None:
        """增强版截图方法
        
        Args:
            page: 页面对象
            name: 截图名称
        """
        screenshot = await page.screenshot(full_page=True, type="png")
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )