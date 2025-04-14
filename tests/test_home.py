import allure
import pytest
import pytest_asyncio
from core.base_test import BaseTest
from pages.home_page import HomePage
from pages.login_page import LoginPage


@allure.feature("首页功能")
class TestHome(BaseTest):
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, page, env):
        """自动初始化fixture"""
        self.config = await self.get_config(env)
        await self.goto(page, env, "/")
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)

    @allure.story("首页Logo验证")
    @pytest.mark.asyncio
    async def test_home_link(self):
        with allure.step('检查Logo可见性'):
            assert await self.home_page.is_home_link_visible()
        with allure.step('点击Logo刷新页面'):
            await self.home_page.navigate_to_home()

    # 其他测试方法移除setup_method调用，参数列表保持为空
    @allure.story("产品链接验证")
    @pytest.mark.asyncio
    async def test_products_link(self):
        with allure.step('检查产品链接可见性'):
            assert await self.home_page.is_products_link_visible()
        with allure.step('点击产品链接'):
            await self.home_page.click_products_link()

    @allure.story("购物车按钮验证")
    @pytest.mark.asyncio
    async def test_view_cart_button(self):
        with allure.step('检查购物车按钮可见性'):
            assert await self.home_page.is_view_cart_button_visible(), "购物车按钮应可见"
        with allure.step('点击购物车按钮'):
            await self.home_page.click_view_cart()

    @allure.story("登录/注册按钮验证")
    @pytest.mark.asyncio
    async def test_login_signup_button(self):
        with allure.step('验证登录按钮可见'):
            assert await self.home_page.is_login_button_visible()      
        with allure.step('点击登录/注册按钮'):
            await self.home_page.click_login_signup_button()
            current_url = await self.home_page.get_current_url()
            assert current_url == f"{self.config['base_url']}/login"       
        with allure.step('验证注册表单可见'):
            assert await self.login_page.is_signup_form_visible()

    @allure.story("测试用例链接验证")
    @pytest.mark.asyncio
    async def test_testcases_link(self):
        with allure.step('检查测试用例链接可见性'):
            assert await self.home_page.is_test_cases_link_visible(), "测试用例链接应可见"
        with allure.step('跳转测试用例页面'):
            await self.home_page.navigate_to_test_cases()

    @allure.story("API文档链接验证")
    @pytest.mark.asyncio
    async def test_api_docs_link(self):
        with allure.step('检查API文档链接可见性'):
            assert await self.home_page.is_api_docs_link_visible(), "API文档链接应可见"
        with allure.step('打开API文档页面'):
            await self.home_page.click_api_docs()


    @allure.story("联系我们按钮验证")
    @pytest.mark.asyncio
    async def test_contact_us_button(self):
        with allure.step('检查联系我们链接可见性'):
            assert await self.home_page.is_contact_us_visible(), "联系我们按钮应可见"
        with allure.step('打开联系我们页面'):
            await self.home_page.click_contact_us()


    @allure.story("YouTube链接验证")
    @pytest.mark.skip(reason="待完善")
    @pytest.mark.asyncio
    async def test_youtube_link(self):
        with allure.step('检查YouTube链接可见性'):
            assert await self.home_page.is_youtube_link_visible(), "YouTube链接应可见"
        with allure.step('打开YouTube'):
            await self.home_page.open_youtube_channel()

