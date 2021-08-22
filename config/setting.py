#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:seting.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

"""
  应用的配置加载项
"""

from configparser import ConfigParser

# 配置文件目录
CONFIG_DIR = "config/config.conf"
CONFIG = ConfigParser()
CONFIG.read(CONFIG_DIR, encoding='utf-8')


class Settings(object):
    # 项目生成的目标路径
    SOURCE_DIR = CONFIG['PARAMETER']['SOURCE_DIR']
    # 生成项目的名称
    PROJECT_NAME = CONFIG['PARAMETER']['PROJECT_NAME']
    # 代码生成模式-database|table-整库模式|多表模式
    CODEGEN_MODE = CONFIG['PARAMETER']['CODEGEN_MODE']
    # 代码生成层级- default|model|controller|resource|static - 全部|模型层|控制器层|接口层|静态资源层
    CODEGEN_LAYER = CONFIG['PARAMETER']['CODEGEN_LAYER']
    # 定义静态资源文件路径
    STATIC_RESOURCE_DIR = CONFIG['PARAMETER']['STATIC_RESOURCE_DIR']

    # 数据库配置
    DIALECT = CONFIG['DATABASE']['DIALECT']
    DRIVER = CONFIG['DATABASE']['DRIVER']
    USERNAME = CONFIG['DATABASE']['USERNAME']
    PASSWORD = CONFIG['DATABASE']['PASSWORD']
    HOST = CONFIG['DATABASE']['HOST']
    PORT = CONFIG['DATABASE']['PORT']
    DATABASE = CONFIG['DATABASE']['DATABASE']

    # model层配置
    MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                             PORT, DATABASE)
    MODEL_VERSION = None if CONFIG['MODEL']['VERSION'] == 'None' else CONFIG['MODEL']['VERSION']
    MODEL_SCHEMA = None if CONFIG['MODEL']['SCHEMA'] == 'None' else CONFIG['MODEL']['SCHEMA']
    MODEL_TABLES = CONFIG['MODEL']['TABLES']
    MODEL_NOVIEWS = None if CONFIG['MODEL']['NOVIEWS'] == 'None' else CONFIG['MODEL']['SCHEMA']
    MODEL_NOINDEXES = CONFIG.getboolean('MODEL', 'NOINDEXES')
    MODEL_NOCONSTRAINTS = CONFIG.getboolean('MODEL', 'NOCONSTRAINTS')
    MODEL_NOJOINED = CONFIG.getboolean('MODEL', 'NOJOINED')
    MODEL_NOINFLECT = CONFIG.getboolean('MODEL', 'NOINFLECT')
    MODEL_NOCLASSES = CONFIG.getboolean('MODEL', 'NOCLASSES')
    MODEL_NOCOMMENTS = CONFIG.getboolean('MODEL', 'NOCOMMENTS')
    MODEL_OUTFILE = CONFIG['MODEL']['OUTFILE']
