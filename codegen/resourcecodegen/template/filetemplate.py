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
"""

    resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 
{imports}


class {className}Resource(Resource):

    # get
    @classmethod
    @swag_from("ymls/{apiName}_get.yml")
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
        parser.add_argument('Page', type=int, location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', type=int, location='args', required=False, help='Size参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        
        res = {className}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 
            
    # delete
    @classmethod
    @swag_from("ymls/{apiName}_delete.yml")
    def delete(cls, {id}=None):
        if {id}:
            kwargs = {{
                '{id}': {id}
            }}
        
        else:
            parser = reqparse.RequestParser()
            {deleteParameter}
            parser.add_argument('{id}', type=str, location='form', required=False, help='{id}参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)
            
        res = {className}Controller.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    @swag_from("ymls/{apiName}_put.yml")
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
    @swag_from("ymls/{apiName}_post.yml")
    def post(cls):
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
{imports}


class {className}OtherResource(Resource):

    pass
"""

    app_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
   定义应用初始化
\"\"\"

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
    # apiversion blueprint register
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
from flasgger import swag_from


class ApiVersionResource(Resource):

    # get the interface of apiversion -- test
    @swag_from("ymls/apiversion_get.yml")
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
from flask_script import Manager
from flask import request, jsonify
from flasgger import Swagger
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.response_code import RET

# 创建flask的app对象
app = create_app("develop")

manager = Manager(app)
swagger = Swagger(app)


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
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response


if __name__ == "__main__":
    manager.run()

"""

    yml_get_template = """{0}_get
---
tags:
 - name: '{0}'
definitions:
 {0}_get_res_data:
  type: object
  properties:
   code:
    type: string
    description: response_code
   message:
    type: string
    description: response_message
   data:
    type: object
    description: response_data
    properties:         {1}
responses:
 200:
  description: response successfully
  schema:
   $ref: '#/definitions/{0}_get_res_data'
"""

    yml_gets_template = """{0}_gets
---
tags:
 - name: '{0}'
parameters:
{1}
definitions:
 {0}_gets_res_data:
  type: object
  properties:
   code:
    type: string
    description: response_code
   message:
    type: string
    description: response_message
   data:
    type: object
    description: response_data
    properties:         {2}
responses:
 200:
  description: response successfully
  schema:
   $ref: '#/definitions/{0}_gets_res_data'
"""

    yml_post_template = """{0}_post
---
tags:
 - name: '{0}'
parameters:
{1}
definitions:
 {0}_post_res_data:
  type: object
  properties:
   code:
    type: string
    description: response_code
   message:
    type: string
    description: response_message
   data:
    type: object
    description: response_data
    properties:         {2}
responses:
 200:
  description: response successfully
  schema:
   $ref: '#/definitions/{0}_post_res_data'
"""

    yml_delete_template = """{0}_delete
---
tags:
 - name: '{0}'
definitions:
 {0}_delete_res_data:
  type: object
  properties:
   code:
    type: string
    description: response_code
   message:
    type: string
    description: response_message
responses:
 200:
  description: response successfully
  schema:
   $ref: '#/definitions/{0}_delete_res_data'
"""

    yml_put_template = """{0}_put
---
tags:
 - name: '{0}'
parameters:
{1}
definitions:
 {0}_put_res_data:
  type: object
  properties:
   code:
    type: string
    description: response_code
   message:
    type: string
    description: response_message
responses:
 200:
  description: response successfully
  schema:
   $ref: '#/definitions/{0}_put_res_data'
"""
