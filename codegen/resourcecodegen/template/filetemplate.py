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

{table_name_all_small}_blueprint = Blueprint("{table_name_little_camel_case}", __name__)

from . import urls
"""

    urls = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

{imports}

api = Api({table_name_all_small}_blueprint)

{resource}
"""

    urls_view = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

{imports}

api = Api({table_name_all_small}_blueprint)

{otherResource}
"""

    resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.{table_name_little_camel_case}Controller import {table_name_big_camel_case}Controller
from utils import commons
from utils.response_code import RET


class {className}Resource(Resource):

    # get
    @classmethod
    def get(cls, {id}=None):
        if {id}:
            kwargs = {{
                '{id}': {id}
            }}

            res = {className}Controller.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        {getParameter}
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = {className}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, {id}=None):
        if {id}:
            kwargs = {{
                '{id}': {id}
            }}

        else:
            parser = reqparse.RequestParser()
            {deleteParameter}
            # Pass in the ID list for multiple deletions
            parser.add_argument('{id}', type=str, location='form', required=False, help='{id}参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

        res = {className}Controller.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, {id}):
        if not {id}:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        {putParameter}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['{id}'] = {id}

        res = {className}Controller.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        \"\"\"
        {className}List: Pass in values in JSON format to batch add
        eg.[{{k1:v1,k2:v2,...}},...]
        \"\"\"
        parser = reqparse.RequestParser()
        parser.add_argument('{className}List', type=str, location='form', required=False, help='{className}List参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('{className}List'):
            res = {className}Controller.add_list(**kwargs)

        else:
            {postParameter}
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = {className}Controller.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
"""

    resource_multi_primary_key = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.{table_name_little_camel_case}Controller import {table_name_big_camel_case}Controller
from utils import commons
from utils.response_code import RET


class {className}Resource(Resource):

    # get
    @classmethod
    def get(cls):
        parser = reqparse.RequestParser()
        {getParameter}
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = {className}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls):
        parser = reqparse.RequestParser()
        {deleteParameter}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = {className}Controller.delete(**kwargs)
        
        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        {putParameter}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = {className}Controller.update(**kwargs)
        
        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        \"\"\"
        {className}List: Pass in values in JSON format to batch add
        eg.[{{k1:v1,k2:v2,...}},...]
        \"\"\"
        parser = reqparse.RequestParser()
        parser.add_argument('{className}List', type=str, location='form', required=False, help='{className}List参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('{className}List'):
            res = {className}Controller.add_list(**kwargs)

        else:
            {postParameter}
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = {className}Controller.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
"""

    other_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource{imports}


class {className}OtherResource(Resource):
{method}
"""

    app_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
   定义应用初始化
\"\"\"

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from . import setting

# 数据库
db = SQLAlchemy()


# 工厂模式创建app应用对象
def create_app(config_name):
    \"\"\"
    创建flask的应用对象
    :param config_name: string 配置模式的名字  （"develop", "product", "test"）
    :return:
    \"\"\"
    
    config_mode = {{
        'develop': 'DevelopSettings',
        'product': 'ProductSettings',
        'test': 'TestSettings'
    }}
    
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    app.config.from_object(getattr(setting, config_mode[config_name]))

    # 使用app初始化db
    db.init_app(app)

    # 利用Flask_session将数据保存的session中
    Session(app)

    # 调用resource层中定义的方法，初始化所有路由(注册)蓝图
    from api_{api_version} import init_router
    init_router(app)
    
    return app
"""

    api_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

{imports}
def init_router(app):
{blueprint_register}
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

    # get the interface of apiversion -- test
    def get(self):
        back_data = {{
            'version': '{apiversion}'
        }}
        return jsonify(code=RET.OK, message='OK', data=back_data)    
"""

    manage = """#!/usr/bin/python3
# -*- coding: utf-8 -*-

\"\"\"
   入口程序
\"\"\"

from app import create_app
from flask_script import Manager, Server
from flask import request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.response_code import RET

# 创建flask的app对象
app = create_app("develop")

# 通过Flask-Script的Manager,Server接管Flask运行
manager = Manager(app)

# 开启Debug模式
manager.add_command("runserver", Server(use_debugger=True))


# 创建全站拦截器,每个请求之前做处理
@app.before_request
def user_require_token():
    # 不需要token验证的请求点列表
    permission = {permission}

    # 如果不是请求上述列表中的接口，需要验证token
    if request.endpoint not in permission:
        # 在请求头上拿到token
        token = request.headers.get("Token")
        if not all([token]):
            return jsonify(code=RET.PARAMERR, message="缺少参数Token或请求非法")

        # 校验token格式正确与过期时间
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except Exception as e:
            app.logger.error(e)
            # 单平台用户登录失效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期')


# 创建全站拦截器，每个请求之后根据请求方法统一设置返回头
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://api.youwebsite.com':
            response.headers["Access-Control-Allow-Origin"] = 'http://api.youwebsite.com'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token,Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response


if __name__ == "__main__":
    manager.run()

"""