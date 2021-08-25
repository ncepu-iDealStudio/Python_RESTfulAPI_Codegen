#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py
# author:jackiex
# datetime:2020/12/2 11:27
# software: PyCharm

'''
   定义应用初始化过程
'''
import logging
from logging.handlers import RotatingFileHandler


from utils.common import ReConverter
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .setting import Settings
from flask_uploads import UploadSet, configure_uploads

# 数据库
db = SQLAlchemy()
# 配置日志信息
# 设置日志的记录等级
"""
开发应用程序或部署开发环境时，可以使用 DEBUG 或 INFO 级别的日志获取尽可能详细的日志信息来进行开发或部署调试；
应用上线或部署生产环境时，应该使用 WARNING 或 ERROR 或 CRITICAL 级别的日志来降低机器的I/O压力和提高获取错误
日志信息的效率。配置文件为DEBUG时会默认设置级别为DEBUG
"""
logging.basicConfig(level=logging.DEBUG)

# 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存日志文件个数上限
file_log_handler = RotatingFileHandler("logs/logs", maxBytes=1024 * 1024 * 100, backupCount=10)

# 创建日志记录格式
formatter = logging.Formatter('%(asctime)s-%(levelname)s %(filename)s:%(lineno)d %(message)s')

# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)

# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)

# 创建flask_uploads对象
"""
UploadSet第一个参数要和配置文件中的“UPLOADED_PHOTOS_DEST”中间的参数相同，第二个参数可以省略，在配置中添加ALLOW设置
"""
images = UploadSet('images', extensions=('jpg', 'png', 'jpeg', 'svg', 'bmp', 'gif'))
files = UploadSet('files', extensions=('txt', 'doc', 'docx', 'pdf', 'avi', 'zip', 'rar', 'mp4','jpg'))

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

    # 为flask补充csrf防护
    # CSRFProtect(app)

    # 为flask-uploads注册app
    # 将 app 的 config 配置注册到 UploadSet 实例 images,同时初始化
    configure_uploads(app, (images, files))

    # 为flask添加自定义得转换器(放在注册蓝图之前)
    app.url_map.converters["re"] = ReConverter

    '''
      整个应用的蓝图加载和注册
    '''

    return app
