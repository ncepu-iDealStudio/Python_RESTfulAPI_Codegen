#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:Nathan
# datetime:2021/8/27 13:19
# software: PyCharm

"""
    this is function description
"""


class FileTemplate(object):
    app_setting = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
  应用的配置加载项
\"\"\"

import os
from configparser import ConfigParser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件和数据文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

CONFIG = ConfigParser()

CONFIG.read(os.path.join(CONFIG_DIR, 'config.conf'), encoding='utf-8')


class Settings(object):
    # 秘钥
    SECRET_KEY = CONFIG['BASIC']['secret_key']
    PUBLIC_KEY = CONFIG['RSA']['public_key']
    PRIVATE_KEY = CONFIG['RSA']['private_key']
    # # debug模式
    # DEBUG = CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

    # 数据库配置
    DIALECT = CONFIG['DATABASE']['dialect']
    DRIVER = CONFIG['DATABASE']['driver']
    USERNAME = CONFIG['DATABASE']['username']
    PASSWORD = CONFIG['DATABASE']['password']
    HOST = CONFIG['DATABASE']['host']
    PORT = CONFIG['DATABASE']['port']
    DATABASE = CONFIG['DATABASE']['database']

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = int(CONFIG['DATABASE']['sqlalchemy_pool_size'])

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = int(CONFIG['DATABASE']['sqlalchemy_max_overflow'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = int(CONFIG['BASIC']['token_expires'])
"""
