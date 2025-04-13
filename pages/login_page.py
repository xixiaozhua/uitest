from typing import Dict, Optional, Tuple

from loguru import logger
from playwright.async_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面对象类，处理登录页面的交互"""

    # 页面元素选择器
    _selectors = {
        # 核心元素 (高优先级)
        "username_input": "#username",  # 用户名输入框
        "password_input": "#password",  # 密码输入框
        "login_button": "button[type='submit']",  # 登录按钮
        "error_message": ".error-message",  # 错误信息
        
        # 重要元素 (中优先级)
        "remember_me": "#remember-me",  # 记住我复选框
        "forgot_password": "a[href*='forgot']",  # 忘记密码链接
        
        # 可选元素 (低优先级)
        "register_link": "a[href*='register']",  # 注册链接
        "language_selector": ".language-selector",  # 语言选择器
    }

    def __init__(self, page: Page):
        """初始化登录页面对象

        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.login_url = "https://example.com/login"  # 默认登录URL
        
        # 从配置文件加载登录URL
        try:
            self.login_url = self._config.get("url", {}).get("login_url", self.login_url)
        except Exception:
            logger.warning("无法从配置文件加载登录URL，使用默认值")

    async def navigate_to_login(self) -> None:
        """导航到登录页面"""
        await self.navigate(self.login_url)
        logger.info(f"导航到登录页面: {self.login_url}")

    async def login(self, username: str, password: str) -> bool:
        """执行登录操作

        Args:
            username: 用户名
            password: 密码

        Returns:
            登录是否成功
        """
        try:
            # 输入用户名和密码
            await self.type_text(self._selectors["username_input"], username)
            await self.type_text(self._selectors["password_input"], password)
            
            # 点击登录按钮
            start_time = self.page.request.timing.request_start
            await self.click(self._selectors["login_button"])
            
            # 等待页面导航完成
            await self.wait_for_navigation()
            
            # 计算API响应时间
            end_time = self.page.request.timing.response_end
            response_time = end_time - start_time if end_time and start_time else 0
            logger.info(f"登录API响应时间: {response_time}ms")
            
            # 检查是否登录成功
            if await self.is_visible(self._selectors["error_message"]):
                error_msg = await self.get_text(self._selectors["error_message"])
                logger.warning(f"登录失败: {error_msg}")
                return False
            else:
                logger.info(f"用户 {username} 登录成功")
                return True
        except Exception as e:
            logger.error(f"登录过程发生异常: {e}")
            await self._take_screenshot(f"login_error_{username}")
            return False

    async def get_login_error(self) -> str:
        """获取登录错误信息

        Returns:
            错误信息文本
        """
        if await self.is_visible(self._selectors["error_message"]):
            return await self.get_text(self._selectors["error_message"])
        return ""

    async def check_remember_me(self, check: bool = True) -> None:
        """设置记住我复选框

        Args:
            check: 是否选中
        """
        try:
            locator = await self.find_element(self._selectors["remember_me"])
            is_checked = await locator.is_checked()
            
            # 如果当前状态与目标状态不一致，则点击复选框
            if is_checked != check:
                await locator.click()
                logger.info(f"设置记住我复选框: {check}")
        except Exception as e:
            logger.error(f"设置记住我复选框失败: {e}")

    async def click_forgot_password(self) -> None:
        """点击忘记密码链接"""
        await self.click(self._selectors["forgot_password"])
        await self.wait_for_navigation()
        logger.info("点击忘记密码链接")

    async def click_register(self) -> None:
        """点击注册链接"""
        await self.click(self._selectors["register_link"])
        await self.wait_for_navigation()
        logger.info("点击注册链接")

    async def get_page_performance(self) -> Dict[str, float]:
        """获取登录页面性能指标

        Returns:
            性能指标字典
        """
        metrics = await self.get_performance_metrics()
        return {
            "dom_content_loaded": metrics.get("DOMContentLoaded", 0),
            "load_event_time": metrics.get("LoadEventTime", 0),
            "first_paint": metrics.get("FirstPaint", 0),
            "first_contentful_paint": metrics.get("FirstContentfulPaint", 0)
        }