# -*- coding: utf-8 -*-
"""
账户创建成功页面对象模块
封装账户创建成功页面的元素定位和操作方法
"""

from core.base_page import BasePage


class AccountCreatedPage(BasePage):
    """
    账户创建成功页面对象，封装页面元素定位和操作方法
    """

    # 页面元素选择器
    ACCOUNT_CREATED_TITLE = "h2[data-qa='account-created']"  # 账户创建成功标题
    CONGRATULATIONS_TEXT = "div.col-sm-9 p:nth-of-type(1)"  # 祝贺文本
    PRIVILEGES_TEXT = "div.col-sm-9 p:nth-of-type(2)"  # 会员特权文本
    CONTINUE_BUTTON = "a[data-qa='continue-button']"  # 继续按钮

    # region 账户创建成功标题操作
    async def get_account_created_title(self) -> str:
        """获取创建成功标题文本"""
        await self.wait_for_visible(self.ACCOUNT_CREATED_TITLE)
        return await self.get_text(self.ACCOUNT_CREATED_TITLE)
    
    async def is_account_created_title_visible(self) -> bool:
        """检查标题是否可见"""
        return await self.is_visible(self.ACCOUNT_CREATED_TITLE)
    # endregion

    # region 祝贺文本操作
    async def get_congratulations_text(self) -> str:
        """获取祝贺文本"""
        await self.wait_for_visible(self.CONGRATULATIONS_TEXT)
        return await self.get_text(self.CONGRATULATIONS_TEXT)
    
    async def is_congratulations_text_visible(self) -> bool:
        """检查祝贺文本是否可见"""
        return await self.is_visible(self.CONGRATULATIONS_TEXT)
    # endregion

    # region 会员特权文本操作
    async def get_privileges_text(self) -> str:
        """获取会员特权文本"""
        await self.wait_for_visible(self.PRIVILEGES_TEXT)
        return await self.get_text(self.PRIVILEGES_TEXT)
    
    async def is_privileges_text_visible(self) -> bool:
        """检查特权文本是否可见"""
        return await self.is_visible(self.PRIVILEGES_TEXT)
    # endregion

    # region 继续按钮操作
    async def click_continue_button(self) -> None:
        """点击继续按钮"""
        # await self.wait_for_clickable(self.CONTINUE_BUTTON)
        await self.click(self.CONTINUE_BUTTON)
    
    async def is_continue_button_visible(self) -> bool:
        """检查继续按钮是否可见"""
        return await self.is_visible(self.CONTINUE_BUTTON)
    # endregion

    # region 组合操作
    async def continue_to_homepage(self) -> None:
        """安全跳转到首页"""
        await self.click_continue_button()
        await self.wait_for_invisible(self.CONTINUE_BUTTON, timeout=5000)
    # endregion
