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

    async def login(self, email: str, password: str) -> None:
        """执行登录操作
        
        Args:
            email: 登录邮箱
            password: 登录密码
        """
        await self.fill(self.LOGIN_EMAIL_INPUT, email)
        await self.fill(self.LOGIN_PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)

    async def signup(self, name: str, email: str) -> None:
        """执行注册操作
        
        Args:
            name: 注册姓名
            email: 注册邮箱
        """
        await self.fill(self.SIGNUP_NAME_INPUT, name)
        await self.fill(self.SIGNUP_EMAIL_INPUT, email)
        await self.click(self.SIGNUP_BUTTON)

    # region 登录表单操作
    async def is_login_form_visible(self) -> bool:
        """检查登录表单是否可见"""
        return await self.is_visible(self.LOGIN_FORM)
    
    async def wait_for_login_form(self, timeout: float = 15.0) -> None:
        """等待登录表单加载"""
        await self.wait_for_visible(self.LOGIN_FORM, timeout)
    # endregion

    # region 登录邮箱操作
    async def input_login_email(self, email: str) -> None:
        """输入登录邮箱"""
        await self.wait_for_editable(self.LOGIN_EMAIL_INPUT)
        await self.type(self.LOGIN_EMAIL_INPUT, email)
    
    async def is_login_email_visible(self) -> bool:
        """检查邮箱输入框是否可见"""
        return await self.is_visible(self.LOGIN_EMAIL_INPUT)
    # endregion

    # region 登录密码操作
    async def input_login_password(self, password: str) -> None:
        """输入登录密码"""
        await self.wait_for_editable(self.LOGIN_PASSWORD_INPUT)
        await self.type(self.LOGIN_PASSWORD_INPUT, password)
    
    async def is_login_password_visible(self) -> bool:
        """检查密码输入框是否可见"""
        return await self.is_visible(self.LOGIN_PASSWORD_INPUT)
    # endregion

    # region 登录按钮操作
    async def click_login_button(self) -> None:
        """点击登录按钮"""
        await self.wait_for_clickable(self.LOGIN_BUTTON)
        await self.click(self.LOGIN_BUTTON)
    
    async def is_login_button_enabled(self) -> bool:
        """检查登录按钮是否可用"""
        return await self.is_enabled(self.LOGIN_BUTTON)
    
    async def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见"""
        return await self.is_visible(self.LOGIN_BUTTON)
    # endregion

    # region 注册表单操作
    async def is_signup_form_visible(self) -> bool:
        """检查注册表单是否可见"""
        return await self.is_visible(self.SIGNUP_FORM)
    
    async def wait_for_signup_form(self, timeout: float = 15.0) -> None:
        """等待注册表单加载"""
        await self.wait_for_visible(self.SIGNUP_FORM, timeout)
    # endregion

    # region 注册姓名操作
    async def input_signup_name(self, name: str) -> None:
        """输入注册姓名"""
        await self.wait_for_editable(self.SIGNUP_NAME_INPUT)
        await self.type(self.SIGNUP_NAME_INPUT, name)
    
    async def is_signup_name_visible(self) -> bool:
        """检查姓名输入框是否可见"""
        return await self.is_visible(self.SIGNUP_NAME_INPUT)
    # endregion

    # region 注册邮箱操作
    async def input_signup_email(self, email: str) -> None:
        """输入注册邮箱"""
        await self.wait_for_editable(self.SIGNUP_EMAIL_INPUT)
        await self.type(self.SIGNUP_EMAIL_INPUT, email)
    
    async def is_signup_email_visible(self) -> bool:
        """检查注册邮箱输入框是否可见"""
        return await self.is_visible(self.SIGNUP_EMAIL_INPUT)
    # endregion

    # region 注册按钮操作
    async def click_signup_button(self) -> None:
        """点击注册按钮"""
        await self.wait_for_clickable(self.SIGNUP_BUTTON)
        await self.click(self.SIGNUP_BUTTON)
    
    async def is_signup_button_enabled(self) -> bool:
        """检查注册按钮是否可用"""
        return await self.is_enabled(self.SIGNUP_BUTTON)
    
    async def is_signup_button_visible(self) -> bool:
        """检查注册按钮是否可见"""
        return await self.is_visible(self.SIGNUP_BUTTON)
    # endregion

    # region 组合操作
    async def complete_login(self, credentials: dict) -> None:
        """完整登录流程
        
        Args:
            credentials: 登录凭证，包含email和password
        """
        await self.input_login_email(credentials['email'])
        await self.input_login_password(credentials['password'])
        await self.click_login_button()
        await self.wait_for_invisible(self.LOGIN_FORM, timeout=15)

    async def complete_signup(self, signup_data: dict) -> None:
        """完整注册初始化流程
        
        Args:
            signup_data: 注册数据，包含name和email
        """
        await self.input_signup_name(signup_data['name'])
        await self.input_signup_email(signup_data['email'])
        await self.click_signup_button()
        await self.wait_for_invisible(self.SIGNUP_FORM, timeout=15)
    # endregion
