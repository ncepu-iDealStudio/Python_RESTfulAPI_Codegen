#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:seting.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

"""
  应用的配置加载项
"""
import datetime
import os
from configparser import ConfigParser
from redis import Redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件和数据文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

CONFIG = ConfigParser()
FDFS_CONFIG = ConfigParser()
REDIS_CONFIG = ConfigParser()

CONFIG.read(os.path.join(CONFIG_DIR, 'config.conf'), encoding='utf-8')
FDFS_CONFIG.read(os.path.join(CONFIG_DIR, 'fastDFS.conf'), encoding='utf-8')
REDIS_CONFIG.read(os.path.join(CONFIG_DIR, 'redis.conf'), encoding='utf-8')


class Settings(object):
    # 秘钥
    SECRET_KEY = CONFIG['STATIC_CONFIG']['SECRET_KEY']
    PUBLIC_KEY = CONFIG['STATIC_CONFIG']['PUBLIC_KEY']
    PRIVATE_KEY = CONFIG['STATIC_CONFIG']['PRIVATE_KEY']
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

    # 图片验证码的redis有效期, 单位：秒
    IMAGE_CODE_REDIS_EXPIRES = int(CONFIG['STATIC_CONFIG']['IMAGE_CODE_REDIS_EXPIRES'])

    # Redis配置
    # REDIS_HOST = REDIS_CONFIG['REDIS']['HOST']
    # REDIS_PORT = REDIS_CONFIG['REDIS']['PORT']
    # REDIS_PASSWORD = REDIS_CONFIG['REDIS']['PASSWORD']

    # Session
    # SESSION_TYPE = 'redis'  # session类型为redis
    # SESSION_REDIS = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)  # Redis对象
    SESSION_PERMANENT = True  # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = False  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
    PERMANENT_SESSION_LIFETIME = 3600

    # 文件存储方式： 1--本地文件系统,   2--云端对象存储
    FILE_STORE_MODE = 1
    # 图片存储服务器路径配置
    IMAGE_SERVER_DEST = CONFIG['FILE']['IMAGES_SERVER']

    # 文件保存路径配置
    UPLOADED_FILES_DEST = CONFIG['FILE']['FILES_DIR']

    # 报告路径配置
    UPLOADED_REPORT_DEST = CONFIG['FILE']['REPORT_FILES_DIR']
    # 报告压缩文件路径配置
    REPORT_ZIPS_DEST = CONFIG['FILE']['REPORT_ZIPS_DIR']
    # 临时文件路径配置
    UPLOADED_TEMP_DEST = CONFIG['FILE']['TEMP_DIR']
    # 图片保存路径配置
    UPLOADED_IMAGES_DEST = CONFIG['FILE']['IMAGES_DIR']
    # 图片模板路径
    IMAGES_Template_DEST = CONFIG['FILE']['IMAGES_Template']
    # 字体模板路径
    IMAGE_FONT_DEST = CONFIG['FILE']['IMAGES_FONTS']
