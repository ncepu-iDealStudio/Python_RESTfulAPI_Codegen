#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:seting.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

"""
  应用的配置加载项
"""

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
    SECRET_KEY = CONFIG['STATIC_CONFIG']['SECRET_KEY']
    # PUBLIC_KEY = CONFIG['STATIC_CONFIG']['PUBLIC_KEY']
    # PRIVATE_KEY = CONFIG['STATIC_CONFIG']['PRIVATE_KEY']
    # debug模式
    DEBUG = CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

    # 数据库配置
    DIALECT = CONFIG['DATABASE']['DIALECT']
    DRIVER = CONFIG['DATABASE']['DRIVER']
    USERNAME = CONFIG['DATABASE']['USERNAME']
    PASSWORD = CONFIG['DATABASE']['PASSWORD']
    HOST = CONFIG['DATABASE']['HOST']
    PORT = CONFIG['DATABASE']['PORT']
    DATABASE = CONFIG['DATABASE']['DATABASE']

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = CONFIG.getboolean('DATABASE', 'SQLALCHEMY_TRACK_MODIFICATIONS')

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = int(CONFIG['DATABASE']['SQLALCHEMY_POOL_SIZE'])

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = int(CONFIG['DATABASE']['SQLALCHEMY_MAX_OVERFLOW'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = int(CONFIG['STATIC_CONFIG']['TOKEN_EXPIRES'])