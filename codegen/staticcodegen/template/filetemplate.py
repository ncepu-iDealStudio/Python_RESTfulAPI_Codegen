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


class Settings(object):
    pass


class DevelopSettings(Settings):
    DEVELOP_CONFIG = ConfigParser()
    DEVELOP_CONFIG.read(os.path.join(CONFIG_DIR, 'develop_config.conf'), encoding='utf-8')

    # 秘钥
    SECRET_KEY = DEVELOP_CONFIG['BASIC']['secret_key']
    PUBLIC_KEY = DEVELOP_CONFIG['RSA']['public_key']
    PRIVATE_KEY = DEVELOP_CONFIG['RSA']['private_key']
    # # debug模式
    # DEBUG = DEVELOP_CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

    # 数据库配置
    DIALECT = DEVELOP_CONFIG['DATABASE']['dialect']
    DRIVER = DEVELOP_CONFIG['DATABASE']['driver']
    USERNAME = DEVELOP_CONFIG['DATABASE']['username']
    PASSWORD = DEVELOP_CONFIG['DATABASE']['password']
    HOST = DEVELOP_CONFIG['DATABASE']['host']
    PORT = DEVELOP_CONFIG['DATABASE']['port']
    DATABASE = DEVELOP_CONFIG['DATABASE']['database']

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = DEVELOP_CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = int(DEVELOP_CONFIG['DATABASE']['sqlalchemy_pool_size'])

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = int(DEVELOP_CONFIG['DATABASE']['sqlalchemy_max_overflow'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = int(DEVELOP_CONFIG['BASIC']['token_expires'])


class TestSettings(Settings):
    TEST_CONFIG = ConfigParser()
    TEST_CONFIG.read(os.path.join(CONFIG_DIR, 'test_config.conf'), encoding='utf-8')
    
    # 秘钥
    SECRET_KEY = TEST_CONFIG['BASIC']['secret_key']
    PUBLIC_KEY = TEST_CONFIG['RSA']['public_key']
    PRIVATE_KEY = TEST_CONFIG['RSA']['private_key']
    
    # # debug模式
    # DEBUG = TEST_CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

    # 数据库配置
    DIALECT = TEST_CONFIG['DATABASE']['dialect']
    DRIVER = TEST_CONFIG['DATABASE']['driver']
    USERNAME = TEST_CONFIG['DATABASE']['username']
    PASSWORD = TEST_CONFIG['DATABASE']['password']
    HOST = TEST_CONFIG['DATABASE']['host']
    PORT = TEST_CONFIG['DATABASE']['port']
    DATABASE = TEST_CONFIG['DATABASE']['database']

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = TEST_CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = int(TEST_CONFIG['DATABASE']['sqlalchemy_pool_size'])

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = int(TEST_CONFIG['DATABASE']['sqlalchemy_max_overflow'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = int(TEST_CONFIG['BASIC']['token_expires'])


class ProductSettings(Settings):
    PRODUCT_CONFIG = ConfigParser()
    PRODUCT_CONFIG.read(os.path.join(CONFIG_DIR, 'product_config.conf'), encoding='utf-8')
    
    # 秘钥
    SECRET_KEY = PRODUCT_CONFIG['BASIC']['secret_key']
    PUBLIC_KEY = PRODUCT_CONFIG['RSA']['public_key']
    PRIVATE_KEY = PRODUCT_CONFIG['RSA']['private_key']

    # 数据库配置
    DIALECT = PRODUCT_CONFIG['DATABASE']['dialect']
    DRIVER = PRODUCT_CONFIG['DATABASE']['driver']
    USERNAME = PRODUCT_CONFIG['DATABASE']['username']
    PASSWORD = PRODUCT_CONFIG['DATABASE']['password']
    HOST = PRODUCT_CONFIG['DATABASE']['host']
    PORT = PRODUCT_CONFIG['DATABASE']['port']
    DATABASE = PRODUCT_CONFIG['DATABASE']['database']

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = PRODUCT_CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = int(PRODUCT_CONFIG['DATABASE']['sqlalchemy_pool_size'])

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = int(PRODUCT_CONFIG['DATABASE']['sqlalchemy_max_overflow'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = int(PRODUCT_CONFIG['BASIC']['token_expires'])
"""
