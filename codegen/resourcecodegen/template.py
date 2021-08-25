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
    init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

from . import urls

{blueprint}
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

from flask_restplus import Resource, reqparse
from flask import g, jsonify
{imports}


class {className}Resource(Resource):

    # query with primary_key
    def get(self, {id}):
        kwargs = {0}
{idCheck}
{getControllerInvoke}

    # delete
    def delete(self, {id}):
        kwargs = {0}
{idCheck}
{deleteControllerInvoke}

    # put
    def put(self, {id}):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{idCheck}
{putControllerInvoke}
"""

    other_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restplus import Resource, reqparse
from flask import g, jsonify
{imports}


class {className}OtherResource(Resource):

    # add
    def post(self):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{postControllerInvoke}

    # list query
    @classmethod
    def get(self):
        parser = reqparse.RequestParser()
{argument}
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)
{getControllerInvoke}
"""


class CodeBlockTemplate():
    """
    代码块（行）模板
    init_: template for __init__.py
    url_: template for urls.py
    resource_: template for resource.py
    other_resource_: template for otherResource.py
    """
    primary_key = '{0}/<int:{1}>'

    parameter = '        parser.add_argument("{0}", type={1}, location="form", required=False, help="{0}参数类型不正确或缺失")\n'

    init_blueprint = '{0}_blueprint = Blueprint("{1}", __name__)'

    urls_imports = """from . import {0}_blueprint
from api_{1}.{2}Resource.{2}Resource import {3}Resource
from api_{1}.{2}Resource.{2}OtherResource import {3}OtherResource"""

    urls_api = 'api = APi({0}_blueprint)'

    urls_resource = 'api.add_resource({0}Resource, "/{1}", endpoint="{2}")'

    urls_other_resource = 'api.add_resource({0}OtherResource, "/{1}s", endpoint="{2}_list")'

    resource_imports = """
from controller.{0}Controller import {0}Controller
from utils import commons
from utils.response_code import RET"""

    resource_id_check = """
        if not {0}:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs["{0}"] = {0}"""

    get_controller_invoke = """
        res = {0}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    resource_delete_controller_invoke = """
        res = {0}Controller.delete(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    resource_put_controller_invoke = """
        res = {0}Controller.update(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    other_resource_post_controller_invoke = """
        res = {0}Controller.add(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""