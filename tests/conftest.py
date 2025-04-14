# -*- coding: utf-8 -*-
"""
测试配置文件
提供测试所需的全局配置和fixture
"""

import os
import pytest
from typing import Generator
from utils.file_read import read_yaml


def pytest_configure(config) -> None:
    """pytest配置钩子
    
    Args:
        config: pytest配置对象
    """
    # 添加自定义标记
    config.addinivalue_line(
        "markers",
        "asyncio: 标记异步测试用例"
    )


@pytest.fixture(scope="session")
def env() -> Generator[str, None, None]:
    """环境配置fixture
    
    Yields:
        str: 环境名称
    """
    env = os.getenv("TEST_ENV", "test")
    yield env


@pytest.fixture(scope="session")
def config(env: str) -> Generator[dict, None, None]:
    """全局配置fixture
    
    Args:
        env: 环境名称
        
    Yields:
        dict: 环境配置
    """
    config = read_yaml('config/env.yaml', env=env)
    yield config 