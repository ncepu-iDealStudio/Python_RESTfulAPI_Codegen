#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/20 15:59
# software: PyCharm

"""
    load public settings and Initialize the parameters
"""

from config.setting import Settings

# 数据库url
model_url = Settings.MODEL_URL

# 项目路径
project_dir = Settings.PROJECT_DIR

# 目标项目路径
target_dir = Settings.TARGET_DIR

# 代码版本
api_version = Settings.API_VERSION

# 数据库方言
dialect = Settings.DIALECT

# 数据库驱动
driver = Settings.DRIVER

# 数据库登录用户名
username = Settings.USERNAME

# 数据库登录密码
password = Settings.PASSWORD

# 数据库ip地址
host = Settings.HOST

# 数据库端口
port = Settings.PORT

# 数据库
database = Settings.DATABASE

# Flasgger模式
flasgger_mode = Settings.FLASGGER_MODE
