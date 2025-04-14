# -*- coding: utf-8 -*-
"""
登录页面对象模块
封装登录页面的元素定位和操作方法
"""

from core.base_page import BasePage


class LoginPage(BasePage):
    """
    登录页面对象，封装登录页面的元素定位和操作方法
    """
    
    # 页面元素选择器
    # 登录
    LOGIN_EMAIL_INPUT = "input[data-qa='login-email']"  # 登录邮箱输入框
    LOGIN_PASSWORD_INPUT = "input[data-qa='login-password']"  # 登录密码输入框
    LOGIN_BUTTON = "button[data-qa='login-button']"  # 登录按钮
    LOGIN_FORM = "div.login-form > form[action='/login']"  # 登录表单

    # 注册
    SIGNUP_NAME_INPUT = "input[data-qa='signup-name']"  # 注册姓名输入框
    SIGNUP_EMAIL_INPUT = "input[data-qa='signup-email']"  # 注册邮箱输入框
    SIGNUP_BUTTON = "button[data-qa='signup-button']"  # 注册按钮
    SIGNUP_FORM = "div.signup-form > form[action='/signup']"  # 注册表单

    async def login(self, email: str, password: str):
        """执行登录操作"""
        await self.fill(self.LOGIN_EMAIL_INPUT, email)
        await self.fill(self.LOGIN_PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)

    async def signup(self, name: str, email: str):
        """执行注册操作"""
        await self.fill(self.SIGNUP_NAME_INPUT, name)
        await self.fill(self.SIGNUP_EMAIL_INPUT, email)
        await self.click(self.SIGNUP_BUTTON)

    async def is_login_form_visible(self) -> bool:
        """检查登录表单是否可见"""
        return await self.is_visible(self.LOGIN_FORM)

    async def is_signup_form_visible(self) -> bool:
        """检查注册表单是否可见"""
        return await self.is_visible(self.SIGNUP_FORM)
