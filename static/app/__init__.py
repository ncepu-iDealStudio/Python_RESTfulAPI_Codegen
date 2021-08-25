#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

'''
   定义应用初始化过程
'''

from utils.common import ReConverter
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .setting import Settings

# 数据库
db = SQLAlchemy()

# 工厂模式创建app应用对象
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: string 配置模式的名字  （"develop", "product"）
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    app.config.from_object(Settings)

    # 使用app初始化db
    db.init_app(app)

    # 利用Flask_session将数据保存的session中
    Session(app)

    # 为flask添加自定义得转换器(放在注册蓝图之前)
    app.url_map.converters["re"] = ReConverter

    '''
      整个应用的蓝图加载和注册
    '''

    return app
