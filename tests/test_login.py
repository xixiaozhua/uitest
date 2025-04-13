import pytest
import allure
from playwright.async_api import async_playwright
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.file_read import read_yaml

config = read_yaml('config/env.yaml', env='test')

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config['headless'])
        page = await browser.new_page()
        await page.goto(config['base_url'], timeout=config['timeout'])
        
        with allure.step('验证登录按钮可见'):
            home_page = HomePage(page)
            assert await home_page.is_login_button_visible()
            
        with allure.step('点击登录/注册按钮'):
            await home_page.click_login_signup_button()
            assert await home_page.get_current_url() == config['base_url'] + '/login'
            
        with allure.step('验证注册表单可见'):
            login_page = LoginPage(page)
            assert await login_page.is_signup_form_visible()            
        await browser.close()
