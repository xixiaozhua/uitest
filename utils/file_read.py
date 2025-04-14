from pathlib import Path
import yaml
from typing import Dict, Any


def read_yaml(file_path: str, env: str = 'test') -> Dict[str, Any]:
    """
    读取yaml文件并返回解析后的数据
    
    Args:
        file_path: yaml文件路径(支持相对路径)
        env: 要读取的环境配置，默认为test
        
    Returns:
        解析后的yaml数据
        
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