# -*- coding: utf-8 -*-
"""
注册页面对象模块
封装注册页面的元素定位和操作方法
"""

from allure import label
from core.base_page import BasePage
from typing import Union


class RegisterPage(BasePage):
    """
    注册页面对象，封装注册页面的元素定位和操作方法
    """
    
    # 页面元素选择器
    # 基本信息
    SIGNUP_FORM = "div.login-form > form[action='/signup']"  # 注册表单
    TITLE_MR = "input[id='id_gender1']"  # 先生称呼单选按钮
    TITLE_MRS = "input[id='id_gender2']"  # 女士称呼单选按钮
    NAME_INPUT = "input[data-qa='name']"  # 姓名输入框
    EMAIL_INPUT = "input[data-qa='email']"  # 邮箱输入框
    PASSWORD_INPUT = "input[data-qa='password']"  # 密码输入框

    # 出生日期
    DAYS_SELECT = "select[data-qa='days']"  # 日期下拉框
    MONTHS_SELECT = "select[data-qa='months']"  # 月份下拉框
    YEARS_SELECT = "select[data-qa='years']"  # 年份下拉框

    # 通讯选项
    NEWSLETTER_CHECKBOX = "input[id='newsletter']"  # 新闻订阅复选框
    SPECIAL_OFFERS_CHECKBOX = "input[id='optin']"  # 特别优惠复选框

    # 地址信息
    FIRST_NAME_INPUT = "input[data-qa='first_name']"  # 名字输入框
    LAST_NAME_INPUT = "input[data-qa='last_name']"  # 姓氏输入框
    COMPANY_INPUT = "input[data-qa='company']"  # 公司名称输入框
    ADDRESS_INPUT = "input[data-qa='address']"  # 地址输入框
    ADDRESS2_INPUT = "input[data-qa='address2']"  # 备用地址输入框
    COUNTRY_SELECT = "select[data-qa='country']"  # 国家下拉框
    STATE_INPUT = "input[data-qa='state']"  # 州/省输入框
    CITY_INPUT = "input[data-qa='city']"  # 城市输入框
    ZIPCODE_INPUT = "input[data-qa='zipcode']"  # 邮编输入框
    MOBILE_NUMBER_INPUT = "input[data-qa='mobile_number']"  # 手机号码输入框

    # 表单和提交按钮
    CREATE_ACCOUNT_BUTTON = "button[data-qa='create-account']"  # 创建账户按钮

    # region 注册表单操作
    async def is_signup_form_visible(self) -> bool:
        """检查注册表单是否可见"""
        return await self.is_visible(self.SIGNUP_FORM)
    
    async def wait_for_signup_form(self, timeout: float = 15.0) -> None:
        """等待注册表单加载"""
        await self.wait_for_visible(self.SIGNUP_FORM, timeout)
    # endregion

    # region 称呼选择操作
    async def click_title_mr(self) -> None:
        """点击先生称呼选项"""
        await self.wait_for_clickable(self.TITLE_MR)
        await self.click(self.TITLE_MR)
    
    async def is_title_mr_visible(self) -> bool:
        """检查先生称呼是否可见"""
        return await self.is_visible(self.TITLE_MR)
    
    async def is_title_mr_checked(self) -> bool:
        """检查先生称呼是否选中"""
        return await self.is_checked(self.TITLE_MR)
    
    async def click_title_mrs(self) -> None:
        """点击女士称呼选项"""
        await self.wait_for_clickable(self.TITLE_MRS)
        await self.click(self.TITLE_MRS)
    
    async def is_title_mrs_visible(self) -> bool:
        """检查女士称呼是否可见"""
        return await self.is_visible(self.TITLE_MRS)
    
    async def is_title_mrs_checked(self) -> bool:
        """检查女士称呼是否选中"""
        return await self.is_checked(self.TITLE_MRS)
    # endregion

    # region 基本信息输入操作
    async def input_name(self, text: str) -> None:
        """输入姓名"""
        await self.wait_for_editable(self.NAME_INPUT)
        await self.type(self.NAME_INPUT, text)
    
    async def is_name_input_visible(self) -> bool:
        """检查姓名输入框是否可见"""
        return await self.is_visible(self.NAME_INPUT)

    async def input_email(self, text: str) -> None:
        """输入邮箱"""
        await self.wait_for_editable(self.EMAIL_INPUT)
        await self.type(self.EMAIL_INPUT, text)
    
    async def is_email_input_visible(self) -> bool:
        """检查邮箱输入框是否可见"""
        return await self.is_visible(self.EMAIL_INPUT)

    async def input_password(self, text: str) -> None:
        """输入密码"""
        await self.wait_for_editable(self.PASSWORD_INPUT)
        await self.type(self.PASSWORD_INPUT, text)
    
    async def is_password_input_visible(self) -> bool:
        """检查密码输入框是否可见"""
        return await self.is_visible(self.PASSWORD_INPUT)
    # endregion

    # region 出生日期选择操作
    async def select_birth_day(self, day: str) -> None:
        """选择出生日"""
        await self.wait_for_clickable(self.DAYS_SELECT)
        await self.select_option(self.DAYS_SELECT, value=day)
    
    async def is_days_select_visible(self) -> bool:
        """检查日期下拉框是否可见"""
        return await self.is_visible(self.DAYS_SELECT)

    async def select_birth_month(self, month: str) -> None:
        """选择出生月"""
        await self.wait_for_clickable(self.MONTHS_SELECT)
        await self.select_option(self.MONTHS_SELECT, value=month)
    
    async def is_months_select_visible(self) -> bool:
        """检查月份下拉框是否可见"""
        return await self.is_visible(self.MONTHS_SELECT)

    async def select_birth_year(self, year: str) -> None:
        """选择出生年"""
        await self.wait_for_clickable(self.YEARS_SELECT)
        await self.select_option(self.YEARS_SELECT, value=year)
    
    async def is_years_select_visible(self) -> bool:
        """检查年份下拉框是否可见"""
        return await self.is_visible(self.YEARS_SELECT)
    # endregion

    # region 通讯选项操作
    async def check_newsletter(self) -> None:
        """勾选新闻订阅"""
        await self.wait_for_clickable(self.NEWSLETTER_CHECKBOX)
        await self.check(self.NEWSLETTER_CHECKBOX)
    
    async def is_newsletter_visible(self) -> bool:
        """检查新闻订阅复选框是否可见"""
        return await self.is_visible(self.NEWSLETTER_CHECKBOX)
    
    async def is_newsletter_checked(self) -> bool:
        """检查新闻订阅是否勾选"""
        return await self.is_checked(self.NEWSLETTER_CHECKBOX)

    async def check_special_offers(self) -> None:
        """勾选特别优惠"""
        await self.wait_for_clickable(self.SPECIAL_OFFERS_CHECKBOX)
        await self.check(self.SPECIAL_OFFERS_CHECKBOX)
    
    async def is_special_offers_visible(self) -> bool:
        """检查特别优惠复选框是否可见"""
        return await self.is_visible(self.SPECIAL_OFFERS_CHECKBOX)
    
    async def is_special_offers_checked(self) -> bool:
        """检查特别优惠是否勾选"""
        return await self.is_checked(self.SPECIAL_OFFERS_CHECKBOX)
    # endregion

    # region 地址信息操作
    async def input_first_name(self, text: str) -> None:
        """输入名字"""
        await self.wait_for_editable(self.FIRST_NAME_INPUT)
        await self.type(self.FIRST_NAME_INPUT, text)
    
    async def is_first_name_visible(self) -> bool:
        """检查名字输入框是否可见"""
        return await self.is_visible(self.FIRST_NAME_INPUT)

    async def input_last_name(self, text: str) -> None:
        """输入姓氏"""
        await self.wait_for_editable(self.LAST_NAME_INPUT)
        await self.type(self.LAST_NAME_INPUT, text)
    
    async def is_last_name_visible(self) -> bool:
        """检查姓氏输入框是否可见"""
        return await self.is_visible(self.LAST_NAME_INPUT)

    async def input_company(self, text: str) -> None:
        """输入公司名称"""
        await self.wait_for_editable(self.COMPANY_INPUT)
        await self.type(self.COMPANY_INPUT, text)
    
    async def is_company_visible(self) -> bool:
        """检查公司输入框是否可见"""
        return await self.is_visible(self.COMPANY_INPUT)

    async def input_address(self, text: str) -> None:
        """输入主要地址"""
        await self.wait_for_editable(self.ADDRESS_INPUT)
        await self.type(self.ADDRESS_INPUT, text)
    
    async def is_address_visible(self) -> bool:
        """检查地址输入框是否可见"""
        return await self.is_visible(self.ADDRESS_INPUT)

    async def input_address2(self, text: str) -> None:
        """输入次要地址"""
        await self.wait_for_editable(self.ADDRESS2_INPUT)
        await self.type(self.ADDRESS2_INPUT, text)
    
    async def is_address2_visible(self) -> bool:
        """检查次要地址输入框是否可见"""
        return await self.is_visible(self.ADDRESS2_INPUT)

    async def select_country(self, country: str) -> None:
        """选择国家"""
        await self.wait_for_clickable(self.COUNTRY_SELECT)
        await self.select_option(self.COUNTRY_SELECT, label=country)
    
    async def is_country_select_visible(self) -> bool:
        """检查国家下拉框是否可见"""
        return await self.is_visible(self.COUNTRY_SELECT)

    async def input_state(self, text: str) -> None:
        """输入州/省"""
        await self.wait_for_editable(self.STATE_INPUT)
        await self.type(self.STATE_INPUT, text)
    
    async def is_state_visible(self) -> bool:
        """检查州/省输入框是否可见"""
        return await self.is_visible(self.STATE_INPUT)

    async def input_city(self, text: str) -> None:
        """输入城市"""
        await self.wait_for_editable(self.CITY_INPUT)
        await self.type(self.CITY_INPUT, text)
    
    async def is_city_visible(self) -> bool:
        """检查城市输入框是否可见"""
        return await self.is_visible(self.CITY_INPUT)

    async def input_zipcode(self, text: str) -> None:
        """输入邮编"""
        await self.wait_for_editable(self.ZIPCODE_INPUT)
        await self.type(self.ZIPCODE_INPUT, text)
    
    async def is_zipcode_visible(self) -> bool:
        """检查邮编输入框是否可见"""
        return await self.is_visible(self.ZIPCODE_INPUT)

    async def input_mobile_number(self, text: str) -> None:
        """输入手机号码"""
        await self.wait_for_editable(self.MOBILE_NUMBER_INPUT)
        await self.type(self.MOBILE_NUMBER_INPUT, text)
    
    async def is_mobile_number_visible(self) -> bool:
        """检查手机输入框是否可见"""
        return await self.is_visible(self.MOBILE_NUMBER_INPUT)
    # endregion

    # region 表单提交操作
    async def click_create_account(self) -> None:
        """点击创建账户按钮"""
        await self.wait_for_clickable(self.CREATE_ACCOUNT_BUTTON)
        await self.click(self.CREATE_ACCOUNT_BUTTON)
    
    async def is_create_account_visible(self) -> bool:
        """检查创建按钮是否可见"""
        return await self.is_visible(self.CREATE_ACCOUNT_BUTTON)
    
    async def is_create_account_enabled(self) -> bool:
        """检查创建按钮是否可用"""
        return await self.is_enabled(self.CREATE_ACCOUNT_BUTTON)
    # endregion

    # region 组合操作
    async def complete_registration(self, name: str, user_data: Union[dict, str]) -> None:
        """完整注册流程
        
        Args:
            name: 用户姓名
            user_data: 用户数据，支持字典或JSON字符串格式
        """
        # 如果是字符串则转换为字典
        if isinstance(user_data, str):
            import json
            user_data = json.loads(user_data)
            
        # 性别选择
        if user_data.get('title', "Mr") == "Mr":
            await self.click_title_mr()
        else:
            await self.click_title_mrs()
        
        # 基本信息
        await self.input_name(name)
        await self.input_password(user_data['password'])
        
        # 出生日期
        await self.select_birth_day(user_data['birth_day'])
        await self.select_birth_month(user_data['birth_month'])
        await self.select_birth_year(user_data['birth_year'])
        
        # 通讯选项
        if user_data.get('newsletter', False):
            await self.check_newsletter()
        if user_data.get('special_offers', False):
            await self.check_special_offers()
        
        # 地址信息
        await self.input_first_name(user_data['first_name'])
        await self.input_last_name(user_data['last_name'])
        await self.input_company(user_data.get('company', ''))
        await self.input_address(user_data['address'])
        await self.input_address2(user_data.get('address2', ''))
        await self.select_country(user_data['country'])
        await self.input_state(user_data['state'])
        await self.input_city(user_data['city'])
        await self.input_zipcode(user_data['zipcode'])
        await self.input_mobile_number(user_data['mobile_number'])
        
        # 提交表单
        await self.click_create_account()
        await self.wait_for_invisible(self.SIGNUP_FORM, timeout=20000)
    # endregion

    