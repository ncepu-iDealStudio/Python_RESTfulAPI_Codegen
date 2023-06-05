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
{other_resource}
"""

    urls_view = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
import json
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
from utils.response_code import RET, error_map_EN
import json


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
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data="id不能为空")

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
            kwargs['{className}List'] = json.loads(kwargs['{className}List'])
            for data in kwargs['{className}List']:
                for key in {sensitive_columns}:
                    data.pop(key, None)
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
import json


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
            kwargs['{className}List'] = json.loads(kwargs['{className}List'])
            for data in kwargs['{className}List']:
                for key in {sensitive_columns}:
                    data.pop(key, None)
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

api.add_resource(ApiVersionResource, '/apiversion', endpoint='Apiversion')  # 测试接口，获取当前接口的版本
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
