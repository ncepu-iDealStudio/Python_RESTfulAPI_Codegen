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
    # model层配置
    MODEL_URL = CONFIG['MODEL']['URL']
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
