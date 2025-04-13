import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--env", 
        action="store", 
        default="test", 
        help="Environment to run tests against (test, prod, etc)"
    )

@pytest.fixture
def env(request):
    return request.config.getoption("--env")