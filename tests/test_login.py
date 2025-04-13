import asyncio
import csv
import os
import time
from datetime import datetime
from typing import Dict, List

import allure
import pytest
from loguru import logger
from playwright.async_api import Page

from pages.login_page import LoginPage
from utils.file_read import read_csv_file


# 读取测试数据
@pytest.fixture(scope="module")
def login_test_data() -> List[Dict[str, str]]:
    """读取登录测试数据"""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "login_cases.csv")
    return read_csv_file(data_path)


@allure.feature("登录功能")
class TestLogin:
    """登录功能测试类"""

    @allure.story("数据驱动登录测试")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("case_data", login_test_data(), ids=lambda x: f"Case {x['case_id']}: {x['description']}")
    async def test_login_with_different_credentials(self, page: Page, case_data: Dict[str, str], test_result_csv: str):
        """使用不同凭据测试登录功能

        Args:
            page: Playwright页面对象
            case_data: 测试数据
            test_result_csv: 测试结果CSV文件路径
        """
        # 记录测试开始时间
        start_time = time.time()
        screenshot_path = ""
        error_message = ""
        
        try:
            # 创建登录页面对象
            login_page = LoginPage(page)
            
            # 导航到登录页面
            with allure.step("导航到登录页面"):
                await login_page.navigate_to_login()
            
            # 提取测试数据
            case_id = case_data["case_id"]
            username = case_data["username"]
            password = case_data["password"]
            expected_result = case_data["expected_result"]
            description = case_data["description"]
            
            # 记录测试信息
            logger.info(f"执行登录测试: Case {case_id} - {description}")
            logger.info(f"用户名: {username}, 密码: {'*' * len(password) if password else '空'}, 预期结果: {expected_result}")
            
            # 执行登录操作
            with allure.step(f"使用用户名 '{username}' 和密码 '{'*' * len(password) if password else '空'}' 登录"):
                login_result = await login_page.login(username, password)
            
            # 获取性能指标
            with allure.step("获取页面性能指标"):
                performance = await login_page.get_page_performance()
                logger.info(f"页面加载时间: {performance.get('dom_content_loaded', 0):.2f}ms")
                logger.info(f"首次内容绘制: {performance.get('first_contentful_paint', 0):.2f}ms")
            
            # 验证登录结果
            with allure.step("验证登录结果"):
                if expected_result == "success":
                    assert login_result is True, f"预期登录成功，但实际登录失败"
                    logger.info("登录成功验证通过")
                else:
                    assert login_result is False, f"预期登录失败，但实际登录成功"
                    error_msg = await login_page.get_login_error()
                    logger.info(f"登录失败验证通过，错误信息: {error_msg}")
                    
                    # 添加错误信息到Allure报告
                    allure.attach(error_msg, name="错误信息", attachment_type=allure.attachment_type.TEXT)
        
        except Exception as e:
            # 测试过程中发生异常
            error_message = str(e)
            logger.error(f"测试执行异常: {e}")
            
            # 截图
            screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"error_case{case_data.get('case_id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # 添加截图到Allure报告
            allure.attach.file(screenshot_path, name="异常截图", attachment_type=allure.attachment_type.PNG)
            
            # 测试失败
            pytest.fail(f"测试执行异常: {e}")
        
        finally:
            # 计算测试耗时
            duration = time.time() - start_time
            logger.info(f"测试耗时: {duration:.2f}秒")
            
            # 更新测试结果CSV
            with open(test_result_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    case_data.get("case_id", "unknown"),
                    "成功" if error_message == "" else "失败",
                    f"{duration:.2f}",
                    error_message,
                    screenshot_path
                ])

    @allure.story("记住我功能")
    @pytest.mark.asyncio
    async def test_remember_me_functionality(self, page: Page, test_result_csv: str):
        """测试记住我功能

        Args:
            page: Playwright页面对象
            test_result_csv: 测试结果CSV文件路径
        """
        # 记录测试开始时间
        start_time = time.time()
        screenshot_path = ""
        error_message = ""
        
        try:
            # 创建登录页面对象
            login_page = LoginPage(page)
            
            # 导航到登录页面
            with allure.step("导航到登录页面"):
                await login_page.navigate_to_login()
            
            # 勾选记住我
            with allure.step("勾选记住我复选框"):
                await login_page.check_remember_me(True)
            
            # 使用有效凭据登录
            with allure.step("使用有效凭据登录"):
                login_result = await login_page.login("valid_user", "valid_pass")
                assert login_result is True, "登录失败"
            
            # 清除cookies并重新导航到登录页面
            with allure.step("清除cookies并重新导航到登录页面"):
                cookies = await page.context.cookies()
                logger.info(f"获取到 {len(cookies)} 个cookies")
                
                # 检查是否存在记住我相关的cookie
                remember_cookie = next((c for c in cookies if "remember" in c["name"].lower()), None)
                assert remember_cookie is not None, "未找到记住我相关的cookie"
                logger.info(f"找到记住我cookie: {remember_cookie['name']}")
        
        except Exception as e:
            # 测试过程中发生异常
            error_message = str(e)
            logger.error(f"测试执行异常: {e}")
            
            # 截图
            screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"remember_me_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # 添加截图到Allure报告
            allure.attach.file(screenshot_path, name="异常截图", attachment_type=allure.attachment_type.PNG)
            
            # 测试失败
            pytest.fail(f"测试执行异常: {e}")
        
        finally:
            # 计算测试耗时
            duration = time.time() - start_time
            logger.info(f"测试耗时: {duration:.2f}秒")
            
            # 更新测试结果CSV
            with open(test_result_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "remember_me",
                    "成功" if error_message == "" else "失败",
                    f"{duration:.2f}",
                    error_message,
                    screenshot_path
                ])

    @allure.story("页面性能测试")
    @pytest.mark.asyncio
    async def test_login_page_performance(self, page: Page, test_result_csv: str):
        """测试登录页面性能

        Args:
            page: Playwright页面对象
            test_result_csv: 测试结果CSV文件路径
        """
        # 记录测试开始时间
        start_time = time.time()
        screenshot_path = ""
        error_message = ""
        
        try:
            # 创建登录页面对象
            login_page = LoginPage(page)
            
            # 导航到登录页面并测量性能
            with allure.step("导航到登录页面并测量性能"):
                await login_page.navigate_to_login()
                
                # 获取性能指标
                performance = await login_page.get_page_performance()
                
                # 记录性能指标
                logger.info(f"DOM内容加载时间: {performance.get('dom_content_loaded', 0):.2f}ms")
                logger.info(f"页面加载完成时间: {performance.get('load_event_time', 0):.2f}ms")
                logger.info(f"首次绘制时间: {performance.get('first_paint', 0):.2f}ms")
                logger.info(f"首次内容绘制时间: {performance.get('first_contentful_paint', 0):.2f}ms")
                
                # 添加性能指标到Allure报告
                for metric, value in performance.items():
                    allure.attach(f"{value:.2f}ms", name=f"性能指标: {metric}", attachment_type=allure.attachment_type.TEXT)
                
                # 验证性能指标
                assert performance.get('dom_content_loaded', float('inf')) < 3000, "DOM内容加载时间过长"
                assert performance.get('first_contentful_paint', float('inf')) < 5000, "首次内容绘制时间过长"
        
        except Exception as e:
            # 测试过程中发生异常
            error_message = str(e)
            logger.error(f"测试执行异常: {e}")
            
            # 截图
            screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"performance_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # 添加截图到Allure报告
            allure.attach.file(screenshot_path, name="异常截图", attachment_type=allure.attachment_type.PNG)
            
            # 测试失败
            pytest.fail(f"测试执行异常: {e}")
        
        finally:
            # 计算测试耗时
            duration = time.time() - start_time
            logger.info(f"测试耗时: {duration:.2f}秒")
            
            # 更新测试结果CSV
            with open(test_result_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "performance",
                    "成功" if error_message == "" else "失败",
                    f"{duration:.2f}",
                    error_message,
                    screenshot_path
                ])