#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:seting.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

"""
  应用的配置加载项
"""

import json
import os
from configparser import ConfigParser

# 配置文件目录
CONFIG_DIR = "config/config.conf"
CONFIG = ConfigParser()
DATABASE_CONFIG_DIR = "config/database.conf"
DATABASE_CONFIG = ConfigParser()
SECURITY_CONFIG_DIR = "config/security.conf"
SECURITY_CONFIG = ConfigParser()


class Settings(object):
    # 读取配置文件
    CONFIG.read(CONFIG_DIR, encoding='utf-8')
    DATABASE_CONFIG.read(DATABASE_CONFIG_DIR, encoding='utf-8')
    SECURITY_CONFIG.read(SECURITY_CONFIG_DIR, encoding='utf-8')

    # 读取json文件
    with open('config/table_rule.json', 'r', encoding='utf-8') as f:
        TABLE_RULE = json.load(f)

    with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
        TYPE_MAPPING = json.load(f)

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
    # 代码生成模式-database|table-整库模式|多表模式
    CODEGEN_MODE = CONFIG['PARAMETER']['CODEGEN_MODE']
    # 代码生成层级- default|model|controller|resource|static - 全部|模型层|控制器层|接口层|静态资源层
    CODEGEN_LAYER = CONFIG['PARAMETER']['CODEGEN_LAYER']
    # 定义静态资源文件路径
    STATIC_RESOURCE_DIR = os.path.join(BASE_DIR, CONFIG['PARAMETER']['STATIC_RESOURCE_DIR'])

    # 读取用户使用的数据库类型
    DATABASE_TYPE = CONFIG['DATABASE']['DATABASE']
    try:
        # 读取数据库配置
        DIALECT = DATABASE_CONFIG[DATABASE_TYPE]['DIALECT']
        DRIVER = DATABASE_CONFIG[DATABASE_TYPE]['DRIVER']
        USERNAME = DATABASE_CONFIG[DATABASE_TYPE]['USERNAME']
        PASSWORD = DATABASE_CONFIG[DATABASE_TYPE]['PASSWORD']
        HOST = DATABASE_CONFIG[DATABASE_TYPE]['HOST']
        PORT = DATABASE_CONFIG[DATABASE_TYPE]['PORT']
        DATABASE = DATABASE_CONFIG[DATABASE_TYPE]['DATABASE']
        SQLALCHEMY_TRACK_MODIFICATIONS = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_TRACK_MODIFICATIONS']
        SQLALCHEMY_POOL_SIZE = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_POOL_SIZE']
        SQLALCHEMY_MAX_OVERFLOW = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_MAX_OVERFLOW']
    except Exception as e:
        raise Exception('数据库类型名{}出错'.format(DATABASE_TYPE))

    # model层配置
    MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                             PORT, DATABASE)
    MODEL_VERSION = None if CONFIG['MODEL']['VERSION'] == 'None' else CONFIG['MODEL']['VERSION']
    MODEL_SCHEMA = None if CONFIG['MODEL']['SCHEMA'] == 'None' else CONFIG['MODEL']['SCHEMA']
    MODEL_TABLES = CONFIG['MODEL']['TABLES']
    MODEL_NOVIEWS = None if CONFIG['MODEL']['NOVIEWS'] == 'None' else CONFIG['MODEL']['SCHEMA']
    try:
        for i in ['NOINDEXES', 'NOCONSTRAINTS', 'NOJOINED', 'NOINFLECT', 'NOCLASSES', 'NOCOMMENTS']:
            MODEL_NOINDEXES = CONFIG.getboolean('MODEL', i)
            MODEL_NOCONSTRAINTS = CONFIG.getboolean('MODEL', i)
            MODEL_NOJOINED = CONFIG.getboolean('MODEL', i)
            MODEL_NOINFLECT = CONFIG.getboolean('MODEL', i)
            MODEL_NOCLASSES = CONFIG.getboolean('MODEL', i)
            MODEL_NOCOMMENTS = CONFIG.getboolean('MODEL', i)
    except Exception as e:
        raise Exception('{}参数不是一个合法的布尔型'.format(i))

    RSA_TABLE_COLUMN = {}
    # security层配置
    if SECURITY_CONFIG['RSA_TABLE_COLUMN']:
        try:
            for table, columns in SECURITY_CONFIG['RSA_TABLE_COLUMN'].items():
                RSA_TABLE_COLUMN[table] = columns.replace(' ', '').split(',')
        except Exception as e:
            raise Exception('RSA_TABLE_COLUMN参数读取失败')

    @classmethod
    def reload(cls):
        # 读取配置文件
        CONFIG.read(CONFIG_DIR, encoding='utf-8')
        DATABASE_CONFIG.read(DATABASE_CONFIG_DIR, encoding='utf-8')
        SECURITY_CONFIG.read(SECURITY_CONFIG_DIR, encoding='utf-8')

        # 读取json文件
        with open('config/table_rule.json', 'r', encoding='utf-8') as f:
            cls.TABLE_RULE = json.load(f)

        with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
            cls.TYPE_MAPPING = json.load(f)

        # 生成项目的名称
        cls.PROJECT_NAME = CONFIG['PARAMETER']['PROJECT_NAME']
        # 项目生成的目标路径
        cls.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 目标目录
        cls.TARGET_DIR = os.path.join(cls.BASE_DIR, CONFIG['PARAMETER']['TARGET_DIR'])
        # 项目目录
        cls.PROJECT_DIR = os.path.join(cls.TARGET_DIR, cls.PROJECT_NAME)
        # 生成项目API的版本
        cls.API_VERSION = CONFIG['PARAMETER']['API_VERSION'].replace('.', '_')
        # 代码生成模式-database|table-整库模式|多表模式
        cls.CODEGEN_MODE = CONFIG['PARAMETER']['CODEGEN_MODE']
        # 代码生成层级- default|model|controller|resource|static - 全部|模型层|控制器层|接口层|静态资源层
        cls.CODEGEN_LAYER = CONFIG['PARAMETER']['CODEGEN_LAYER']
        # 定义静态资源文件路径
        cls.STATIC_RESOURCE_DIR = os.path.join(cls.BASE_DIR, CONFIG['PARAMETER']['STATIC_RESOURCE_DIR'])

        # 读取用户使用的数据库类型
        cls.DATABASE_TYPE = CONFIG['DATABASE']['DATABASE']
        try:
            # 读取数据库配置
            cls.DIALECT = DATABASE_CONFIG[cls.DATABASE_TYPE]['DIALECT']
            cls.DRIVER = DATABASE_CONFIG[cls.DATABASE_TYPE]['DRIVER']
            cls.USERNAME = DATABASE_CONFIG[cls.DATABASE_TYPE]['USERNAME']
            cls.PASSWORD = DATABASE_CONFIG[cls.DATABASE_TYPE]['PASSWORD']
            cls.HOST = DATABASE_CONFIG[cls.DATABASE_TYPE]['HOST']
            cls.PORT = DATABASE_CONFIG[cls.DATABASE_TYPE]['PORT']
            cls.DATABASE = DATABASE_CONFIG[cls.DATABASE_TYPE]['DATABASE']
            cls.SQLALCHEMY_TRACK_MODIFICATIONS = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_TRACK_MODIFICATIONS']
            cls.SQLALCHEMY_POOL_SIZE = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_POOL_SIZE']
            cls.SQLALCHEMY_MAX_OVERFLOW = DATABASE_CONFIG['DEFAULT']['SQLALCHEMY_MAX_OVERFLOW']
        except Exception as e:
            raise Exception('数据库类型名{}出错'.format(cls.DATABASE_TYPE))

        # model层配置
        cls.MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            cls.DIALECT,
            cls.DRIVER,
            cls.USERNAME,
            cls.PASSWORD,
            cls.HOST,
            cls.PORT,
            cls.DATABASE
        )
        cls.MODEL_VERSION = None if CONFIG['MODEL']['VERSION'] == 'None' else CONFIG['MODEL']['VERSION']
        cls.MODEL_SCHEMA = None if CONFIG['MODEL']['SCHEMA'] == 'None' else CONFIG['MODEL']['SCHEMA']
        cls.MODEL_TABLES = CONFIG['MODEL']['TABLES']
        cls.MODEL_NOVIEWS = None if CONFIG['MODEL']['NOVIEWS'] == 'None' else CONFIG['MODEL']['SCHEMA']
        try:
            for i in ['NOINDEXES', 'NOCONSTRAINTS', 'NOJOINED', 'NOINFLECT', 'NOCLASSES', 'NOCOMMENTS']:
                cls.MODEL_NOINDEXES = CONFIG.getboolean('MODEL', i)
                cls.MODEL_NOCONSTRAINTS = CONFIG.getboolean('MODEL', i)
                cls.MODEL_NOJOINED = CONFIG.getboolean('MODEL', i)
                cls.MODEL_NOINFLECT = CONFIG.getboolean('MODEL', i)
                cls.MODEL_NOCLASSES = CONFIG.getboolean('MODEL', i)
                cls.MODEL_NOCOMMENTS = CONFIG.getboolean('MODEL', i)
        except Exception as e:
            raise Exception('{}参数不是一个合法的布尔型'.format(i))

        cls.RSA_TABLE_COLUMN = {}
        # security层配置
        if SECURITY_CONFIG['RSA_TABLE_COLUMN']:
            try:
                for table, columns in SECURITY_CONFIG['RSA_TABLE_COLUMN'].items():
                    cls.RSA_TABLE_COLUMN[table] = columns.replace(' ', '').split(',')
            except Exception as e:
                raise Exception('RSA_TABLE_COLUMN参数读取失败')
