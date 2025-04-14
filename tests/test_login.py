# -*- coding: utf-8 -*-
"""
登录功能测试模块
测试用户登录功能的可用性
"""

import allure
import pytest
from core.base_test import BaseTest
from pages.home_page import HomePage
from pages.login_page import LoginPage


@allure.feature("用户登录")
class TestLogin(BaseTest):
    """登录功能测试套件"""

    @allure.story("登录流程验证")
    @pytest.mark.asyncio
    async def test_login_flow(self, page, env) -> None:
        """验证完整登录流程
        
        Args:
            page: 页面对象
            env: 环境名称
        """
        config = await self.get_config(env)
        
        await self.goto(page, env, "/")
        
        with allure.step('验证登录按钮可见'):
            home_page = HomePage(page)
            assert await home_page.is_login_button_visible()
            
        with allure.step('点击登录/注册按钮'):
            await home_page.click_login_signup_button()
            current_url = await home_page.get_current_url()
            assert current_url == f"{config['base_url']}/login"
            
        with allure.step('验证注册表单可见'):
            login_page = LoginPage(page)
            assert await login_page.is_signup_form_visible()

