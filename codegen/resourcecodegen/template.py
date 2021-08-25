#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:template.py
# author:PigKinght
# datetime:2021/8/24 21:55
# software: PyCharm

"""
    the template file define.
"""


class FileTemplate():
    """

    """
    template_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

from . import urls

{blueprint}
"""

    template_urls = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

{imports}

{api}

{resource}

{otherResource}
"""

    template_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restplus import Resource, reqparse
from flask import g, jsonify
{imports}


class {className}Resource(Resource):

    # query with primary_key
    @classmethod
    def get(cls, {id}):
        kwargs = {0}
{idCheck}
{getControllerInvoke}

    # delete
    @classmethod
    def delete(cls, {id}):
        kwargs = {0}
{idCheck}
{deleteControllerInvoke}

    # put
    @classmethod
    def put(cls, {id}):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{idCheck}
{putControllerInvoke}
"""

    template_other_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restplus import Resource, reqparse
from flask import g, jsonify
{imports}


class {className}OtherResource(Resource):

    # add
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{postControllerInvoke}

    # list query
    @classmethod
    def get(cls):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{getControllerInvoke}
"""



class CodeBlockTemplate():
    """
    代码块（行）模板
    url_:为生成url.py文件定义的模板；

    """
    blueprint_format = '{0}_blueprint = Blueprint("{1}", __name__)'

    urls_imports_format = """from . import {0}_blueprint
from api_1.{1}Resource.{1}Resource import {2}Resource
from api_1.{1}Resource.{1}OtherResource import {2}OtherResource"""

    api_format = 'api = APi({0}_blueprint)'

    primary_key_format = '/<int:{0}>'

    resource_format = 'api.add_resource({0}Resource, "{1}", endpoint="{2}")'

    other_resource_format = 'api.add_resource({0}OtherResource, "", endpoint="{1}_list")'

    resource_imports_format = """
from controller.{0}Controller import {0}Controller
from utils import commons
from utils.response_code import RET"""

    id_check_format = """
        if not {0}:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs["{0}"] = {0}"""

    arguement_format = '        parser.add_argument("{0}", type={1}, location="form", required=False, help="{0}参数类型不正确或缺失")\n'

    get_controller_invoke_format = """
        res = {0}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    delete_controller_invoke_format = """
        res = {0}Controller.delete(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    put_controller_invoke_format = """
        res = {0}Controller.put(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    post_controller_invoke_format = """
        res = {0}Controller.add(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""