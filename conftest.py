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
