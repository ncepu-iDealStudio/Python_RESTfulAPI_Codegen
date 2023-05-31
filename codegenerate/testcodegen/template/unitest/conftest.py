#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    存放fixture固件的配置文件
"""

import os

import pytest

from test.unitest.utils.read_env import read_env


@pytest.fixture(scope="function")
def env_dict():
    """获得环境变量字典"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_dict = read_env(env_path)
    return env_dict
