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
    PASSWORD = CONFIG['DATABASE']['PASSWORD']
    HOST = CONFIG['DATABASE']['HOST']
    PORT = CONFIG['DATABASE']['PORT']
    DATABASE = CONFIG['DATABASE']['DATABASE']

    # model层配置
    MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                             PORT, DATABASE)

# os.chdir(os.path.dirname(os.path.dirname(__file__)))
#
# config_file_dir = 'config'
#
#
# class Settings(object):
#     """
#         加载读取json格式的配置文件
#     """
#
#     @classmethod
#     def load(cls, setting_name=None) -> None:
#         """
#             加载指定配置文件
#             加载完后配置存储为类属性
#             :param setting_name: 配置文件名(无后缀)
#         """
#
#         if setting_name is None:
#             config_dir = config_file_dir + '/default.json'
#         else:
#             config_dir = config_file_dir + '/' + setting_name + '.json'
#
#         with open(config_dir, 'r', encoding='utf-8') as fr:
#             settings = json.load(fr)
#             for key, value in settings.items():
#                 if key in ['database', 'model']:
#                     for neo_key, neo_value in value.items():
#                         setattr(cls, neo_key.upper(), neo_value)
#                 else:
#                     setattr(cls, key.upper(), value)
#
#         with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
#             cls.TYPE_MAPPING = json.load(f)
#
#         cls.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#         cls.TARGET_DIR = os.path.join(cls.BASE_DIR, cls.TARGET_DIR)
#         cls.PROJECT_DIR = os.path.join(cls.TARGET_DIR, cls.PROJECT_NAME)
#         cls.API_VERSION = cls.API_VERSION.replace('.', '_')
#         cls.MODEL_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
#             cls.DIALECT,
#             cls.DRIVER,
#             cls.USERNAME,
#             cls.PASSWORD,
#             cls.HOST,
#             cls.PORT,
#             cls.DATABASE
#         )
#         cls.TABLE_RULE = {
#             'table_record_delete_logic_way': settings['table_record_delete_logic_way'],
#             'table_business_key_gen_rule': settings['table_business_key_gen_rule']
#         }
#         database_type = {
#             'mysql': 'DEFAULT',
#             'postgresql': 'PostgreSQL',
#             'mssql': 'SQL Server',
#             'oracle': 'Oracle'
#         }
#         cls.DATABASE_TYPE = database_type.get(cls.DIALECT, 'DEFAULT')
#
#     @classmethod
#     def save(cls, setting_name: str) -> None:
#         """
#             将配置存储至指定文件
#             :param setting_name: 指定文件名(无后缀)
#         """
#
#         if setting_name == 'default':
#             raise Exception('存储目标文件与默认配置同名！！！')
#
#         # 获取应存储的属性名
#         attr_list = dir(cls)
#         attr_list = [attr for attr in attr_list if attr.isupper() and attr not in [
#                 'BASE_DIR', 'PROJECT_DIR', 'MODEL_URL', 'TYPE_MAPPING', 'TABLE_RULE', 'DATABASE_TYPE'
#             ]]
#
#         # 将要保存的配置属性存储到字典中
#         save_dict = {
#             'database': {},
#             'model': {}
#         }
#         for attr in attr_list:
#             if attr in [
#                 'DIALECT', 'DRIVER', 'USERNAME', 'PASSWORD', 'HOST', 'PORT', 'DATABASE',
#                 'SQLALCHEMY_TRACK_MODIFICATIONS', 'SQLALCHEMY_POOL_SIZE', 'SQLALCHEMY_MAX_OVERFLOW'
#             ]:
#                 save_dict['database'][attr.lower()] = getattr(cls, attr)
#             elif attr in [
#                 'MODEL_VERSION', 'MODEL_SCHEMA', 'MODEL_TABLES', 'MODEL_NOVIEWS', 'MODEL_NOINDEXES',
#                 'MODEL_NOCONSTRAINTS', 'MODEL_NOJOINED', 'MODEL_NOINFLECT', 'MODEL_NOCLASSES',
#                 'MODEL_NOCOMMENTS', 'MODEL_NOREFLECT'
#             ]:
#                 save_dict['model'][attr.lower()] = getattr(cls, attr)
#             elif attr == 'TARGET_DIR':
#                 save_dict[attr.lower()] = getattr(cls, attr).split('Python_RESTfulAPI_Codegen\\')[-1]
#             else:
#                 save_dict[attr.lower()] = getattr(cls, attr)
#
#         # 写入文件中
#         setting_dir = config_file_dir + '/' + setting_name + '.json'
#         with open(setting_dir, 'w', encoding='utf-8') as fw:
#             fw.write(json.dumps(save_dict))
