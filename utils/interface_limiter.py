#!/user/bin/env python3
# -*- coding:utf-8 -*-

# file:interface_limiter.py
# author:Superclass
# datetime:2022/5/23 12:32
# software: PyCharm
'''
    获取全局接口访问频率限制器
'''
import json
import os

from flask import make_response, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class InterfaceLimiter(object):
    # 读取限制器有关配置
    app = None
    default_limits = None
    error_message = None

    @classmethod
    def get_settings(cls):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CONFIG_PATH = os.path.join(BASE_DIR, "config/limiter.json")
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        cls.default_limits = settings['default_limits']
        cls.second_limit = settings['second_limit']
        cls.minute_limit = settings['minute_limit']
        cls.hour_limit = settings['hour_limit']
        cls.day_limit = settings['day_limit']

    # 获取限制器，进行初始化
    @classmethod
    def get_limiter(cls, app):
        cls.get_settings()
        cls.app = app
        limiter = Limiter(
            cls.app,
            key_func=get_remote_address,
            default_limits=cls.default_limits
        )
        app.register_error_handler(429, cls.limiter_error_handler)

        return limiter

    # 限制超出时的错误页面，注册路由方法
    @classmethod
    def limiter_error_handler(cls, e):
        return cls.app.send_static_file('429.html')

