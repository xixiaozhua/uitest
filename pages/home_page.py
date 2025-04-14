# -*- coding: utf-8 -*-
"""
首页页面对象模块
封装页面的元素定位和操作方法
"""

from core.base_page import BasePage


class HomePage(BasePage):
    """
    首页页面对象，封装页面的元素定位和操作方法
    """

    # 页面元素选择器
    PRODUCTS_LINK = "a[href='/products']"  # 产品页链接
    VIEW_CART_BUTTON = "a[href='/view_cart']"  # 购物车查看按钮
    LOGIN_SIGNUP_BUTTON = "a[href='/login']"  # 登录/注册按钮
    LOGOUT_BUTTON = "a[href='/logout']"  # 登出按钮
    DELETE_ACCOUNT_BUTTON = "a[href='/delete_account']"  # 删除账户
    TEST_CASES_LINK = "a[href='/test_cases']"  # 测试用例页链接
    API_LIST_LINK = "a[href='/api_list']"  # API文档页链接
    YOUTUBE_CHANNEL_LINK = "a[href='https://www.youtube.com/c/AutomationExercise']"  # YouTube频道链接
    CONTACT_US_BUTTON = "a[href='/contact_us']"  # 联系我们按钮
    HOME_LINK = "a[href='/']"  # 首页Logo链接

    async def is_login_button_visible(self) -> bool:
        """检查登录/注册按钮是否可见"""
        return await self.is_visible(self.LOGIN_SIGNUP_BUTTON)
        
    async def click_login_signup_button(self) -> None:
        """点击登录/注册按钮"""
        await self.click(self.LOGIN_SIGNUP_BUTTON)

    # region 产品页链接操作
    async def is_products_link_visible(self) -> bool:
        """检查产品链接是否可见"""
        return await self.is_visible(self.PRODUCTS_LINK)
    
    async def click_products_link(self) -> None:
        """点击产品链接"""
        await self.click(self.PRODUCTS_LINK)
    # endregion

    # region 购物车按钮操作
    async def is_view_cart_button_visible(self) -> bool:
        """检查购物车按钮是否可见"""
        return await self.is_visible(self.VIEW_CART_BUTTON)
    
    async def click_view_cart(self) -> None:
        """点击购物车按钮"""
        await self.click(self.VIEW_CART_BUTTON)
    # endregion

    # region 测试用例链接操作
    async def is_test_cases_link_visible(self) -> bool:
        """检查测试用例链接是否可见"""
        return await self.is_visible(self.TEST_CASES_LINK)
    
    async def navigate_to_test_cases(self) -> None:
        """跳转测试用例页面"""
        await self.click(self.TEST_CASES_LINK)
    # endregion

    # region API文档链接操作
    async def is_api_docs_link_visible(self) -> bool:
        """检查API文档链接是否可见"""
        return await self.is_visible(self.API_LIST_LINK)
    
    async def click_api_docs(self) -> None:
        """点击API文档按钮"""
        await self.click(self.API_LIST_LINK)
    # endregion

    # region YouTube频道链接操作
    async def is_youtube_link_visible(self) -> bool:
        """检查YouTube链接是否可见"""
        return await self.is_visible(self.YOUTUBE_CHANNEL_LINK)
    
    async def open_youtube_channel(self) -> None:
        """访问YouTube频道（返回新页面对象）"""
        async with self.page.context.expect_page() as new_page:
            await self.click(self.YOUTUBE_CHANNEL_LINK)
        return await new_page.value
    # endregion

    # region 联系我们按钮操作
    async def is_contact_us_visible(self) -> bool:
        """检查联系我们按钮是否可见"""
        return await self.is_visible(self.CONTACT_US_BUTTON)
    
    async def click_contact_us(self) -> None:
        """点击联系我们按钮"""
        await self.click(self.CONTACT_US_BUTTON)
    # endregion

    # region 首页Logo链接操作
    async def is_home_link_visible(self) -> bool:
        """检查首页Logo是否可见"""
        return await self.is_visible(self.HOME_LINK)
    
    async def navigate_to_home(self) -> None:
        """通过Logo返回首页"""
        await self.click(self.HOME_LINK)
    # endregion

    # region 登出按钮操作
    async def click_logout_button(self) -> None:
        """点击登出按钮"""
        await self.wait_for_clickable(self.LOGOUT_BUTTON)
        await self.click(self.LOGOUT_BUTTON)
    
    async def is_logout_button_visible(self) -> bool:
        """检查登出按钮是否可见"""
        return await self.is_visible(self.LOGOUT_BUTTON)
    # endregion

    # region 删除账户操作
    async def click_delete_account_button(self) -> None:
        """点击删除账户按钮"""
        await self.wait_for_clickable(self.DELETE_ACCOUNT_BUTTON)
        await self.click(self.DELETE_ACCOUNT_BUTTON)
    
    async def is_delete_account_button_visible(self) -> bool:
        """检查删除按钮是否可见"""
        return await self.is_visible(self.DELETE_ACCOUNT_BUTTON)
    # endregion
        
