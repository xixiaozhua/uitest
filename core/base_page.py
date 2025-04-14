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

    async def goto(self, url: str, timeout: float) -> None:
        """导航到指定URL
        
        Args:
            url: 目标URL
            timeout: 超时时间（毫秒）
        """
        await self.page.goto(url, timeout=timeout)

    async def click(self, selector: str) -> None:
        """点击指定元素
        
        Args:
            selector: 元素选择器
        """
        await self.page.click(selector)

    async def fill(self, selector: str, text: str) -> None:
        """在输入框中填写文本
        
        Args:
            selector: 元素选择器
            text: 要填写的文本
        """
        await self.page.fill(selector, text)

    async def is_visible(self, selector: str, timeout=30000) -> bool:
        """检查元素是否可见
        
        Args:
            selector: 元素选择器
            
        Returns:
            bool: 元素是否可见
        """
        return await self.page.is_visible(selector, timeout=timeout)

    async def wait_for_selector(self, selector: str, timeout: float = 30000) -> None:
        """等待元素出现
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认30000
        """
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def wait_for_visible(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可见
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认15000
        """
        await self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    async def wait_for_clickable(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可点击
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认15000
        """
        element = self.page.locator(selector)
        await element.wait_for(state="visible", timeout=timeout)
        await self.page.wait_for_function(
            "(element) => element.disabled === false",
            arg=await element.element_handle(),
            timeout=timeout
        )

    async def wait_for_editable(self, selector: str, timeout: float = 15000) -> None:
        """等待元素可编辑
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认15000
        """
        await self.wait_for_visible(selector, timeout)
        await self.wait_for_clickable(selector, timeout)

    async def wait_for_invisible(self, selector: str, timeout: float = 30000) -> None:
        """等待元素不可见
        
        Args: 
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认15000
        """
        await self.page.locator(selector).wait_for(state="hidden", timeout=timeout)

    async def get_text(self, selector: str) -> str:
        """获取元素的文本内容
        
        Args:
            selector: 元素选择器
            
        Returns:
            str: 元素的文本内容
        """
        return await self.page.text_content(selector)

    async def get_attribute(self, selector: str, attribute: str) -> str:
        """获取元素的属性值
        
        Args:
            selector: 元素选择器
            attribute: 属性名
            
        Returns:
            str: 属性值
        """
        return await self.page.get_attribute(selector, attribute)

    async def screenshot(self, path: str) -> None:
        """截取页面截图
        
        Args:
            path: 截图保存路径
        """
        await self.page.screenshot(path=path)
        
    async def get_current_url(self) -> str:
        """获取当前页面URL
        
        Returns:
            str: 当前页面URL
        """
        return self.page.url

    async def is_present(self, selector: str) -> bool:
        """检查元素是否存在
        
        Args:
            selector: 元素选择器
            
        Returns:
            bool: 元素是否存在
        """
        return await self.page.locator(selector).count() > 0

    async def type(self, selector: str, text: str, delay: float = 0.1) -> None:
        """输入文本（带可编辑状态等待）
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
            delay: 输入延迟（秒），默认0.1
        """
        await self.wait_for_editable(selector)
        await self.page.locator(selector).type(text, delay=delay)

    async def is_enabled(self, selector: str) -> bool:
        """检查元素是否启用
        
        Args:
            selector: 元素选择器
            
        Returns:
            bool: 元素是否启用
        """
        return await self.page.locator(selector).is_enabled()

    async def is_disabled(self, selector: str) -> bool:
        """检查元素是否被禁用
        
        Args:
            selector: 元素选择器
            
        Returns:
            bool: 元素是否被禁用
        """
        return await self.page.locator(selector).is_disabled()

    async def is_checked(self, selector: str) -> bool:
        """检查复选框/单选按钮是否被选中
        
        Args:
            selector: 元素选择器
            
        Returns:
            bool: 元素是否被选中
        """
        return await self.page.locator(selector).is_checked()

    async def check(self, selector: str) -> None:
        """勾选复选框/单选按钮（带安全等待）
        
        Args:
            selector: 元素选择器
        """
        await self.wait_for_clickable(selector)
        await self.page.locator(selector).check()

    async def select_option(self, selector: str, **kwargs) -> None:
        """选择下拉框选项（带安全等待）
        
        Args:
            selector: 元素选择器
            **kwargs: 支持value/index/label参数，如value='1' 或 label='北京'
        """
        await self.wait_for_clickable(selector)
        await self.page.locator(selector).select_option(**kwargs)