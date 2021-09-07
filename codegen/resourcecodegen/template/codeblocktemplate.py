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
    primary_key = '{0}/<int:{1}>'

    parameter_args = '        parser.add_argument("{0}", type={1}, location="args", required=False, help="{0}参数类型不正确或缺失")\n'

    parameter_form = '        parser.add_argument("{0}", type={1}, location="form", required=False, help="{0}参数类型不正确或缺失")\n'
    init_blueprint = '{0}_blueprint = Blueprint("{1}", __name__)'

    urls_imports = """from . import {0}_blueprint
from api_{1}.{2}Resource.{2}Resource import {3}Resource
from api_{1}.{2}Resource.{2}OtherResource import {3}OtherResource"""

    urls_api = 'api = Api({0}_blueprint)'

    urls_resource = 'api.add_resource({0}Resource, "/{1}", endpoint="{2}")'

    urls_other_resource = 'api.add_resource({0}OtherResource, "/{1}s", endpoint="{1}_list")'

    urls_service_resource = """
# joint query
@{0}_blueprint.route('/{1}/query', methods=['GET'], endpoint='{1}_query')
def {2}_query():
    return {2}OtherResource.joint_query()
"""

    resource_imports = """
from controller.{0}Controller import {1}Controller
from utils import commons
from utils.response_code import RET"""

    resource_id_check = """
        if not {0}:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs["{0}"] = {0}"""

    resource_get_controller_invoke = """
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

    other_resource_get_controller_invoke = """
        res = {0}Controller.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], count=res['count'], pages=res['pages'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    other_resource_imports = """
from controller.{0}Controller import {1}Controller
from service.{0}Service import {1}Service
from utils import commons
from utils.response_code import RET"""

    other_resource_post_controller_invoke = """
        res = {0}Controller.add(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    other_resource_get_service_invoke = """
        res = {0}Service.joint_query(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], count=res['count'], pages=res['pages'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])"""

    app_init_blueprint = """
    # {0} blueprint register
    from api_{1}.{0}Resource import {2}_blueprint
    app.register_blueprint({2}_blueprint, url_prefix="/api_{1}")
    """

    yml_data_template = """
         {0}:
          type: {1}
          description: {0}"""

    yml_get_parameter_template = """
         - name: {0}
           in: query
           type: {1}
           description: {0}
           required: false"""

    yml_post_parameter_template = """
         - name: {0}
           in: body
           type: {1}
           description: {0}
           required: true"""

    yml_put_parameter_template = """
             - name: {0}
               in: body
               type: {1}
               description: {0}
               required: false"""