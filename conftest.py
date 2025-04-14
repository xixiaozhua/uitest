import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="运行环境: test/staging/prod"
    )

@pytest.fixture(scope="session")
def env(request):
    """获取测试环境配置"""
    return request.config.getoption("--env")

@pytest.fixture(scope="function")
async def page(browser_context):
    """增强版页面fixture"""
    page = await browser_context.new_page()
    page.set_default_timeout(30000)
    
    # 添加页面初始操作
    await page.add_init_script(script="""// 防机器人检测脚本 """)
    
    yield page
    
    # 统一资源清理
    if not page.is_closed():
        await page.context.clear_cookies()
        await page.close()
