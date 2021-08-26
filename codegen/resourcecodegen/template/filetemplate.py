#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:PigKinght
# datetime:2021/8/26 10:55
# software: PyCharm

"""
    the template file define.
"""


class FileTemplate():
    """
    init_: template for api_x/init__.py
    url_: template for api_x/urls.py
    resource_: template for api_x/resource.py
    other_resource_: template for api_x/otherResource.py
    app_init_: template for app/__init__.py
    app_setting_: template for app/__setting__.py
    """
    init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

{blueprint}

from . import urls
"""

    urls = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

{imports}

{api}

{resource}

{otherResource}
"""

    resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import g, jsonify
{imports}


class {className}Resource(Resource):

    # query with primary_key
    def get(self, {id}):
        kwargs = {{}}
{idCheck}
{getControllerInvoke}

    # delete
    def delete(self, {id}):
        kwargs = {{}}
{idCheck}
{deleteControllerInvoke}

    # put
    def put(self, {id}):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{idCheck}
{putControllerInvoke}
"""

    other_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify
{imports}


class {className}OtherResource(Resource):

    # add
    def post(self):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{postControllerInvoke}

    # list query
    def get(self):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{getControllerInvoke}
"""

    app_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
   定义应用初始化过程
'''

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .setting import Settings

# 数据库
db = SQLAlchemy()

# 工厂模式创建app应用对象
def create_app(config_name):
    \"\"\"
    创建flask的应用对象
    :param config_name: string 配置模式的名字  （"develop", "product"）
    :return:
    \"\"\"
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    app.config.from_object(Settings)

    # 使用app初始化db
    db.init_app(app)

    # 利用Flask_session将数据保存的session中
    Session(app)

    '''
      整个应用的蓝图加载和注册
    '''
    # classInfo blueprint register
    {blueprint_register}
    return app
"""

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

CONFIG = ConfigParser()

CONFIG.read(os.path.join(CONFIG_DIR, 'config.conf'), encoding='utf-8')


class Settings(object):
    # 秘钥
    SECRET_KEY = CONFIG['STATIC_CONFIG']['SECRET_KEY']
    # PUBLIC_KEY = CONFIG['STATIC_CONFIG']['PUBLIC_KEY']
    # PRIVATE_KEY = CONFIG['STATIC_CONFIG']['PRIVATE_KEY']
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
"""

    api_version_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

apiversion_blueprint = Blueprint("apiversion", __name__)

from . import urls
"""

    api_version_urls = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
from . import apiversion_blueprint
from api_{apiversion}.apiVersionResource.apiVersionResource import ApiVersionResource

api = Api(apiversion_blueprint)

api.add_resource(ApiVersionResource, '/apiversion', endpoint='apiversion')  # 测试接口，获取当前接口的版本
"""

    api_version_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify
from utils.response_code import RET


class ApiVersionResource(Resource):

    # get the interface of apiVersion -- test
    @classmethod
    def get(self):
        back_data = {{
            'version': '{apiversion}'
        }}
        return jsonify(code=RET.OK, message='OK', data=back_data)    
"""
