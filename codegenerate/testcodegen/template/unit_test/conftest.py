import os

import pytest
import requests
from loguru import logger

from test.unit_test.utils.read_env import read_env, write_env
from test.unit_test.utils.record import record_log_allure


# def pytest_addoption(parser):
#     parser.addoption("--version-test", action="store_true", default=None, help="Specify the API version to test")

@pytest.fixture(scope="function")
def env_dict():
    """获得环境变量字典"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_dict = read_env(env_path)
    # record_log_allure("env_dict", env_dict)
    return env_dict


@pytest.fixture(scope="module")
def get_and_write_token():
    """获得登录前置"""
    # 创建一个session对象，用于维持登录状态
    session = requests.Session()

    # 在session对象中进行登录操作
    login_url = "http://127.0.0.1:5000/api_1_0/sysUser/login"
    login_data = {
        "account": "pytest",
        "password": "pytest"
    }
    response = session.post(login_url, data=login_data)

    try:
        res_data = response.json()
    except ValueError as e:
        logger.exception("响应数据不是有效的JSON格式")
        raise ValueError("响应数据不是有效的JSON格式")

    env_path = os.path.join(os.path.dirname(__file__), '.env')

    try:
        login_token = res_data['data'].get('token', None)
        write_env(env_path, login_token)
    except KeyError as e:
        logger.exception("登录失败，未获取到token")
        raise KeyError("登录失败，未获取到token")
