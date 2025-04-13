import yaml

import os

def read_yaml(file_path, env='test'):
    """
    读取yaml文件并返回解析后的数据
    :param file_path: yaml文件路径(支持相对路径)
    :param env: 要读取的环境配置，默认为test
    :return: 解析后的yaml数据
    """
    abs_path = os.path.join(os.path.dirname(__file__), '..', file_path)
    with open(abs_path, 'r') as f:
        data = yaml.safe_load(f)
        return data.get(env, {})