#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    this is function description
"""


def read_env(env_path) -> dict:
    """
        1. 格式key=value
        2. 支持#注释
    :param: .env文件路径
    :return: 环境变量字典
    """
    env_dict = {}
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.replace(" ", "").split('=')
                env_dict[key] = value.strip()
    return env_dict
