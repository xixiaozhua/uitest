from re import A
import allure
import pytest
import pytest_asyncio
from core.base_test import BaseTest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.account_created_page import AccountCreatedPage


@allure.feature("用户注册")
class TestRegister(BaseTest):
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, page, env):
        """自动初始化fixture"""
        self.config = await self.get_config(env)
        self.register_data = await self.get_data('register_data.csv')
        await self.goto(page, env, "/login")
        self.login_page = LoginPage(page)
        self.register_page = RegisterPage(page)
        self.account_created_page = AccountCreatedPage(page)
        self.home_page = HomePage(page)

    @allure.story("注册流程验证")
    @pytest.mark.asyncio
    async def test_login_flow(self):
        with allure.step('验证姓名、邮箱输入框、注册按钮可见'):
            assert await self.login_page.is_signup_name_visible()
            assert await self.login_page.is_signup_email_visible()
            assert await self.login_page.is_signup_button_visible()
            
        with allure.step('输入姓名、邮箱'):
            await self.login_page.input_signup_name(self.register_data[0]['name'])
            await self.login_page.input_signup_email(self.register_data[0]['email'])
            await self.login_page.click_signup_button()
            
        with allure.step('验证注册表单各配置项可见'):
            assert await self.register_page.is_signup_form_visible()
            assert await self.register_page.is_title_mr_visible()
            assert await self.register_page.is_title_mrs_visible()
            assert await self.register_page.is_name_input_visible()
            assert await self.register_page.is_password_input_visible()
            assert await self.register_page.is_email_input_visible()
            assert await self.register_page.is_email_input_disabled()  # 验证邮箱输入框不可编辑
            assert await self.register_page.is_password_input_visible()
            assert await self.register_page.is_days_select_visible()
            assert await self.register_page.is_months_select_visible()
            assert await self.register_page.is_years_select_visible()
            assert await self.register_page.is_special_offers_visible()
            assert await self.register_page.is_newsletter_visible()
            assert await self.register_page.is_special_offers_visible()
            assert await self.register_page.is_first_name_visible()
            assert await self.register_page.is_last_name_visible()
            assert await self.register_page.is_company_visible()
            assert await self.register_page.is_address_visible()
            assert await self.register_page.is_address2_visible()
            assert await self.register_page.is_country_select_visible()
            assert await self.register_page.is_state_visible()
            assert await self.register_page.is_city_visible()
            assert await self.register_page.is_zipcode_visible()
            assert await self.register_page.is_mobile_number_visible()
            assert await self.register_page.is_create_account_visible()

        with allure.step('填写各配置项'):
            await self.register_page.complete_registration(self.register_data[0]['name'], self.register_data[0]['user_data'])
        
        with allure.step('验证账户创建成功页面各配置项可见'):
            assert await self.account_created_page.is_account_created_title_visible()
            assert await self.account_created_page.is_congratulations_text_visible()
            assert await self.account_created_page.is_privileges_text_visible()
            assert await self.account_created_page.is_continue_button_visible()
        
        with allure.step('点击继续按钮'):
            await self.account_created_page.click_continue_button()

        with allure.step('验证登出、删除账号按钮可见'):
            assert await self.home_page.is_logout_button_visible()
            assert await self.home_page.is_delete_account_button_visible()