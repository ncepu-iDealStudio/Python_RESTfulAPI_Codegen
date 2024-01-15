#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:configResource.py
# author:jackiex
# datetime:2024/1/15 15:58
# software: PyCharm

'''
    配置文件管理资源
'''

from flask_restful import Resource

class ConfigResource(Resource):

    @classmethod
    def write_user_config(cls, config):
        # 写入配置文件
        with open('config.ini', 'w') as f:
            f.write(config)

    @classmethod
    def read_user_config(cls):
        # 读取配置文件
        with open('config.ini', 'r') as f:
            config = f.read()
        return config

    @classmethod
    def get_user_config(cls):
        # 获取配置文件内容
        config = cls.read_config()
        return config




