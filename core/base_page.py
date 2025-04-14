# -*- coding: utf-8 -*-
"""
基础页面对象模块
封装Playwright异步API的基本页面操作方法
"""

from playwright.async_api import Page

class BasePage:
    """
    基础页面对象，封装Playwright异步API的基本页面操作方法
    """

    def __init__(self, page: Page):
        self.page = page

    async def goto(self, url: str, timeout):
        """导航到指定URL"""
        await self.page.goto(url, timeout)

    async def click(self, selector: str):
        """点击指定元素"""
        await self.page.click(selector)

    async def fill(self, selector: str, text: str):
        """在输入框中填写文本"""
        await self.page.fill(selector, text)

    async def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        return await self.page.is_visible(selector)

    async def wait_for_selector(self, selector: str, timeout: float = 30000):
        """等待元素出现"""
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def get_text(self, selector: str) -> str:
        """获取元素的文本内容"""
        return await self.page.text_content(selector)

    async def get_attribute(self, selector: str, attribute: str) -> str:
        """获取元素的属性值"""
        return await self.page.get_attribute(selector, attribute)

    async def screenshot(self, path: str):
        """截取页面截图"""
        await self.page.screenshot(path=path)
        
    async def get_current_url(self) -> str:
        """获取当前页面URL"""
        return self.page.url