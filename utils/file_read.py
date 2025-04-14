# -*- coding: utf-8 -*-
"""
文件读取工具模块
提供YAML和CSV文件的读取功能
"""

import csv
from pathlib import Path
import yaml
from typing import Dict, Any, List


def read_yaml(file_path: str, env: str = 'test') -> Dict[str, Any]:
    """读取yaml文件并返回解析后的数据
    
    Args:
        file_path: yaml文件路径(支持相对路径)
        env: 要读取的环境配置，默认为test
        
    Returns:
        Dict[str, Any]: 解析后的yaml数据
        
    Raises:
        FileNotFoundError: 当文件不存在时
        yaml.YAMLError: 当yaml解析失败时
    """
    try:
        abs_path = Path(__file__).parent.parent / file_path
        if not abs_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {abs_path}")
            
        with open(abs_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get(env, {})
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"YAML解析错误: {str(e)}")


def read_csv(file_path: str, has_header: bool = True) -> List[Dict[str, Any]]:
    """读取CSV文件并返回解析后的数据
    
    Args:
        file_path: CSV文件路径(支持相对路径)
        has_header: 是否有表头，默认为True
        
    Returns:
        List[Dict[str, Any]]: 解析后的CSV数据列表
        
    Raises:
        FileNotFoundError: 当文件不存在时
        csv.Error: 当CSV解析失败时
    """
    try:
        abs_path = Path(__file__).parent.parent / file_path
        if not abs_path.exists():
            raise FileNotFoundError(f"数据文件不存在: {abs_path}")
            
        with open(abs_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f) if has_header else csv.reader(f)
            return list(reader)
    except csv.Error as e:
        raise csv.Error(f"CSV解析错误: {str(e)}")