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

{serviceResource}
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
{parameter}
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
{parameter1}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{postControllerInvoke}

    # list query
    def get(self):
        parser = reqparse.RequestParser()
{parameter1}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{getControllerInvoke}

    # join table query
    def join_table_query(self):
        parser = reqparse.RequestParser()
{parameter2}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
{getServiceInvoke}
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
