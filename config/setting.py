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
from urllib import parse

os.chdir(os.path.dirname(os.path.dirname(__file__)))

# 配置文件目录
CONFIG_DIR = "config/config.conf"
CONFIG = ConfigParser()


class Settings(object):
    # 读取配置文件
    CONFIG.read(CONFIG_DIR, encoding='utf-8')

    # 生成项目的名称
    PROJECT_NAME = CONFIG['PARAMETER']['PROJECT_NAME']
    # 项目生成的目标路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 目标目录
    TARGET_DIR = os.path.join(BASE_DIR, CONFIG['PARAMETER']['TARGET_DIR'])
    # 项目目录
    PROJECT_DIR = os.path.join(TARGET_DIR, PROJECT_NAME)
    # 生成项目API的版本
    API_VERSION = CONFIG['PARAMETER']['API_VERSION'].replace('.', '_')
    # 定义静态资源文件路径
    STATIC_RESOURCE_DIR = os.path.join(BASE_DIR, 'static')

    # 数据库dialect到driver的映射
    driver_dict = {
        'mysql': 'pymysql',
        'mssql': 'pymssql',
        'oracle': 'cx_oracle',
        'postgresql': 'psycopg2'
    }

    # 读取数据库配置
    DIALECT = CONFIG['DATABASE']['DIALECT']
    DRIVER = driver_dict[DIALECT]
    USERNAME = CONFIG['DATABASE']['USERNAME']
    PASSWORD = parse.quote_plus(CONFIG['DATABASE']['PASSWORD'])
    HOST = CONFIG['DATABASE']['HOST']
    PORT = CONFIG['DATABASE']['PORT']
    DATABASE = CONFIG['DATABASE']['DATABASE']

    # model层配置
    MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT,
        DRIVER,
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        DATABASE
    )
