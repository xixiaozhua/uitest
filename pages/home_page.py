# -*- coding: utf-8 -*-
"""
首页页面对象模块
封装页面的元素定位和操作方法
"""

from pages.base_page import BasePage


class HomePage(BasePage):
    """
    首页页面对象，封装页面的元素定位和操作方法
    """

    # 页面元素选择器
    # head区块
    LOGIN_SIGNUP_BUTTON = "a[href='/login']"  # 登录/注册按钮


    async def is_login_button_visible(self) -> bool:
        """检查登录/注册按钮是否可见"""
        return await self.is_visible(self.LOGIN_SIGNUP_BUTTON)
        
    async def click_login_signup_button(self):
        """点击登录/注册按钮"""
        await self.click(self.LOGIN_SIGNUP_BUTTON)
        
