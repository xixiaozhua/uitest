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

    async def wait_for_visible(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可见（单位：毫秒）"""
        await self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    async def wait_for_clickable(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可点击（单位：毫秒）"""
        element = self.page.locator(selector)
        await element.wait_for(state="visible", timeout=timeout)
        await element.wait_for(
            lambda loc: loc.is_enabled(),
            timeout=timeout
        )

    async def wait_for_editable(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可编辑（单位：毫秒）"""
        await self.wait_for_visible(selector, timeout)
        await self.wait_for_clickable(selector, timeout)

    async def wait_for_invisible(self, selector: str, timeout: float = 15000) -> None:
        """等待元素不可见（单位：毫秒）"""
        await self.page.locator(selector).wait_for(state="hidden", timeout=timeout)

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

    async def is_present(self, selector: str) -> bool:
        """检查元素是否存在"""
        return await self.page.locator(selector).count() > 0

    async def type(self, selector: str, text: str, delay: float = 0.1) -> None:
        """输入文本（带可编辑状态等待）"""
        await self.wait_for_editable(selector)
        await self.page.locator(selector).type(text, delay=delay)

    async def wait_for_clickable(self, selector: str, timeout: float = 15.0) -> None:
        """等待元素可点击"""
        element = self.page.locator(selector)
        # 转换秒为毫秒
        await element.wait_for(state="visible", timeout=timeout*1000)
        await self.page.wait_for_function(
            "(element) => element.disabled === false",
            arg=await element.element_handle(),
            timeout=timeout*1000  # 转换为毫秒
        )

    async def is_enabled(self, selector: str) -> bool:
        """检查元素是否启用"""
        return await self.page.locator(selector).is_enabled()

    async def is_disabled(self, selector: str) -> bool:
        """检查元素是否被禁用"""
        return await self.page.locator(selector).is_disabled()

    async def is_checked(self, selector: str) -> bool:
        """检查复选框/单选按钮是否被选中"""
        return await self.page.locator(selector).is_checked()

    async def check(self, selector: str) -> None:
        """勾选复选框/单选按钮（带安全等待）"""
        await self.wait_for_clickable(selector)
        await self.page.locator(selector).check()

    async def select_option(self, selector: str, **kwargs) -> None:
        """选择下拉框选项（带安全等待）
        :param kwargs: 支持value/index/label参数，如value='1' 或 label='北京'
        """
        await self.wait_for_clickable(selector)
        await self.page.locator(selector).select_option(**kwargs)