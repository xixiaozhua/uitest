import asyncio
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import yaml
from loguru import logger
from playwright.async_api import ElementHandle, Locator, Page, expect


class BasePage:
    """页面对象基类，提供所有页面通用的方法和属性"""

    def __init__(self, page: Page):
        """初始化基础页面对象

        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.timeout = 30000  # 默认超时时间(毫秒)
        self.retry_count = 3  # 元素定位失败重试次数
        self.retry_interval = 1  # 重试间隔(秒)

        # 从配置文件加载环境变量
        self._load_config()

    def _load_config(self) -> None:
        """从配置文件加载环境变量"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "env.yaml")
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                self.timeout = config.get("browser", {}).get("timeout", self.timeout)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")

    async def navigate(self, url: str) -> None:
        """导航到指定URL

        Args:
            url: 目标URL
        """
        start_time = time.time()
        try:
            await self.page.goto(url, wait_until="networkidle")
            load_time = time.time() - start_time
            logger.info(f"页面加载完成: {url}, 耗时: {load_time:.2f}秒")
        except Exception as e:
            logger.error(f"导航到 {url} 失败: {e}")
            await self._take_screenshot(f"navigate_error_{int(time.time())}")
            raise

    async def find_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """查找元素，支持自动重试

        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间

        Returns:
            Playwright Locator对象
        """
        actual_timeout = timeout or self.timeout
        locator = self.page.locator(selector).first

        # 记录元素定位轨迹
        logger.debug(f"尝试定位元素: {selector}")

        for attempt in range(self.retry_count):
            try:
                # 等待元素可见
                await expect(locator).to_be_visible(timeout=actual_timeout)
                logger.debug(f"成功定位元素: {selector}")
                return locator
            except Exception as e:
                if attempt < self.retry_count - 1:
                    logger.warning(f"定位元素 {selector} 失败，第 {attempt + 1} 次重试: {e}")
                    await asyncio.sleep(self.retry_interval)
                else:
                    logger.error(f"定位元素 {selector} 失败，已达最大重试次数: {e}")
                    await self._take_screenshot(f"element_not_found_{int(time.time())}")
                    raise

    async def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """点击元素

        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间
        """
        try:
            locator = await self.find_element(selector, timeout)
            # 等待元素稳定（确保元素不在移动或变化）
            await self._wait_for_element_stable(locator)
            await locator.click()
            logger.info(f"点击元素: {selector}")
        except Exception as e:
            logger.error(f"点击元素 {selector} 失败: {e}")
            await self._take_screenshot(f"click_error_{int(time.time())}")
            raise

    async def type_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """在输入框中输入文本

        Args:
            selector: 元素选择器
            text: 要输入的文本
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间
        """
        try:
            locator = await self.find_element(selector, timeout)
            await locator.fill(text)
            logger.info(f"在元素 {selector} 中输入文本")
        except Exception as e:
            logger.error(f"在元素 {selector} 中输入文本失败: {e}")
            await self._take_screenshot(f"type_text_error_{int(time.time())}")
            raise

    async def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取元素文本

        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间

        Returns:
            元素文本内容
        """
        try:
            locator = await self.find_element(selector, timeout)
            text = await locator.text_content()
            return text or ""
        except Exception as e:
            logger.error(f"获取元素 {selector} 文本失败: {e}")
            await self._take_screenshot(f"get_text_error_{int(time.time())}")
            raise

    async def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否可见

        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间

        Returns:
            元素是否可见
        """
        try:
            locator = self.page.locator(selector).first
            return await locator.is_visible(timeout=timeout or self.timeout)
        except Exception:
            return False

    async def wait_for_navigation(self, timeout: Optional[int] = None) -> None:
        """等待页面导航完成

        Args:
            timeout: 超时时间(毫秒)，默认使用页面默认超时时间
        """
        try:
            actual_timeout = timeout or self.timeout
            await self.page.wait_for_load_state("networkidle", timeout=actual_timeout)
            logger.info("页面导航完成")
        except Exception as e:
            logger.error(f"等待页面导航超时: {e}")
            await self._take_screenshot(f"navigation_timeout_{int(time.time())}")
            raise

    async def _wait_for_element_stable(self, locator: Locator, check_interval: int = 100, stability_threshold: int = 3) -> None:
        """等待元素稳定（位置不再变化）

        Args:
            locator: 元素定位器
            check_interval: 检查间隔(毫秒)
            stability_threshold: 稳定阈值(次数)
        """
        stable_count = 0
        last_rect = None

        while stable_count < stability_threshold:
            try:
                # 获取元素位置和大小
                current_rect = await locator.bounding_box()
                
                if current_rect is None:
                    # 元素不可见，重置稳定计数
                    stable_count = 0
                elif last_rect is None:
                    # 首次获取位置
                    last_rect = current_rect
                    stable_count = 1
                elif (abs(last_rect["x"] - current_rect["x"]) < 1 and
                      abs(last_rect["y"] - current_rect["y"]) < 1 and
                      abs(last_rect["width"] - current_rect["width"]) < 1 and
                      abs(last_rect["height"] - current_rect["height"]) < 1):
                    # 位置稳定，增加稳定计数
                    stable_count += 1
                else:
                    # 位置变化，重置稳定计数
                    stable_count = 1
                    last_rect = current_rect
                
                await asyncio.sleep(check_interval / 1000)
            except Exception:
                # 获取位置失败，重置稳定计数
                stable_count = 0
                await asyncio.sleep(check_interval / 1000)

    async def _take_screenshot(self, name: str) -> str:
        """截取当前页面截图

        Args:
            name: 截图名称

        Returns:
            截图保存路径
        """
        try:
            # 确保截图目录存在
            screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # 生成截图文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            # 保存截图
            await self.page.screenshot(path=filepath, full_page=True)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """获取页面性能指标

        Returns:
            性能指标字典
        """
        try:
            # 获取性能指标
            metrics = {}
            client = await self.page.context.new_cdp_session(self.page)
            performance = await client.send("Performance.getMetrics")
            
            # 提取关键指标
            for metric in performance["metrics"]:
                metrics[metric["name"]] = metric["value"]
            
            # 记录关键性能指标
            logger.info(f"页面加载时间: {metrics.get('DOMContentLoaded', 0):.2f}ms")
            return metrics
        except Exception as e:
            logger.error(f"获取性能指标失败: {e}")
            return {}