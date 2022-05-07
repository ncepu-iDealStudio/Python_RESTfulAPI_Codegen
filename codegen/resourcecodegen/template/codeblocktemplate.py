#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codeblocktemplate.py
# author:PigKinght
# datetime:2021/8/24 21:55
# software: PyCharm

"""
    the template code block define.
"""


class CodeBlockTemplate():
    """
    init_: template for api_x/__init__.py
    url_: template for api_x/urls.py
    resource_: template api_x/for resource.py
    other_resource_: template for api_x/otherResource.py
    app_init_: template for api_x/app.__init__.py
    """

    primary_key_single = '"/{0}/<{1}>", "/{0}"'

    primary_key_multi = '"/{0}"'

    parameter_2 = '''parser.add_argument("{column}", location="{location}", required={required}, help="{column}参数类型不正确或缺失")
        '''

    parameter_3 = '''parser.add_argument("{column}", location="{location}", required={required}, help="{column}参数类型不正确或缺失")
            '''

    urls_imports_table = """from . import {0}_blueprint
from api_{1}.{2}Resource.{2}Resource import {3}Resource
from api_{1}.{2}Resource.{2}OtherResource import {3}OtherResource"""

    urls_imports_view = """from . import {0}_blueprint
from api_{1}.{2}Resource.{2}OtherResource import {3}OtherResource"""

    urls_resource = 'api.add_resource({0}Resource, {1}, endpoint="{0}")'

    urls_other_resource = """
# joint query
@{0}_blueprint.route('/{1}/query', methods=['GET'], endpoint='{2}Query')
def {2}_query():
    return {2}OtherResource.joint_query()
"""

    other_resource_imports = """, reqparse
from flask import jsonify

from service.{0}Service import {1}Service
from utils import commons
from utils.response_code import RET"""

    other_resource_query = """
    @classmethod
    def joint_query(cls):
        parser = reqparse.RequestParser()
        {0}
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        
        res = {1}Service.joint_query(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalCount=res['totalCount'], totalPage=res['totalPage'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])"""

    api_init_blueprint = """
    # {0} blueprint register
    from api_{1}.{0}Resource import {2}_blueprint
    app.register_blueprint({2}_blueprint, url_prefix="/api_{1}")
    """

    api_init_imports = 'from .{0}Resource import {1}_blueprint\n'
