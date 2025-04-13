import csv
import os
from typing import Dict, List, Optional

import yaml
from loguru import logger


def read_csv_file(file_path: str) -> List[Dict[str, str]]:
    """读取CSV文件并返回字典列表

    Args:
        file_path: CSV文件路径

    Returns:
        字典列表，每个字典代表一行数据，键为列名
    """
    try:
        # 确保文件路径是绝对路径
        if not os.path.isabs(file_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, file_path)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return []

        # 读取CSV文件
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    except Exception as e:
        logger.error(f"读取CSV文件失败: {e}")
        return []


def read_yaml_file(file_path: str) -> Dict:
    """读取YAML文件并返回字典

    Args:
        file_path: YAML文件路径

    Returns:
        字典，包含YAML文件内容
    """
    try:
        # 确保文件路径是绝对路径
        if not os.path.isabs(file_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, file_path)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return {}

        # 读取YAML文件
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"读取YAML文件失败: {e}")
        return {}