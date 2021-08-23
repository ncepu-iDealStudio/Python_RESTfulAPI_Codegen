#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen.py
# author:PigKnight
# datetime:2021/8/23 8:45
# software: PyCharm

"""
this is function description
"""
from sqlalchemy.types import INTEGER, SMALLINT, VARCHAR, NUMERIC
import sys

mysql_map = {INTEGER: type(int), SMALLINT: type(int), VARCHAR: type(str), NUMERIC: type(float)}

# 连字符转驼峰
def str_format_convert(s):
    ss = ''
    for i in s.split('_'):
        if ss:
            ss += i.lower().capitalize()
        else:
            ss = i
    return ss


# 数据库字段类型对应python数据类型


class CodeGenerator(object):
    template_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

from . import urls

{api}
    """

    template_urls = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restplus import Api
{importStr}

{api}

{resource}

{otherResource}
"""

    template_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restplus import Resource, reqparse
from flask import g, jsonify

{importStr}

class {className}Resource(Resource):

    # 根据业务主键查询
    @classmethod
    def get(cls{id}):
        parser = reqparse.RequestParser()
        {argument}
        kwargs = parser.parse_args()
        kwargs = commans.put_remove_none(*kwargs)
        
        {idCheck}
        
        {controllerInvoke}
    
    # 修改
    @classmethod
    def put(cls{id}):
        parser = reqparse.RequestParser()
        {argument}
        kwargs = parser.parse_args()
        kwargs = commans.put_remove_none(*kwargs)
        
        {idCheck}
        
        {controllerInvoke}
    
    # 删除
    @classmethod
    def delete(cls{id}):
        parser = reqparse.RequestParser()
        {argument}
        kwargs = parser.parse_args()
        kwargs = commans.put_remove_none(*kwargs)
        
        {idCheck}
        
        {controllerInvoke}
"""

    template_other_resource = """
    #!/usr/bin/env python
    # -*- coding:utf-8 -*-
    
    {import}
    
    {classOther}
    
    # 添加
    @classmethod
    def add():
        parser = reqparse.RequestParser()
        {argument}
        kwargs = parser.parse_args()
        kwargs = commans.put_remove_none(*kwargs)
        
        {controllerInvoke}
    
    # 列表查询
    @classmethod
    def get():
        parser = reqparse.RequestParser()
        {argument}
        kwargs = parser.parse_args()
        kwargs = commans.put_remove_none(*kwargs)
        
        {idCheck}
        
        {controllerInvoke}
    """

    def __init__(self, metadata, template_init=None, template_urls=None, template_resource=None,
                 template_other_resource=None):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata
        if template_init:
            self.template = template_init
        if template_urls:
            self.template_urls = template_urls
        if template_resource:
            self.template_resource = template_resource
        if template_other_resource:
            self.template_other_resource = template_other_resource

    # 生成resource层
    def resource_generator(self, outfile=sys.stdout):
        # 获取表列表
        table_names = self.metadata.tables.values()
        table_dict = {}
        for i in table_names:
            # 获得表
            table_dict[str(i)] = {}
            table_dict[str(i)]['columns'] = {}
            for j in i.c.values():
                # 获得字段属性
                # table_dict[str(i)].append((j.key, j.type, j.primary_key))
                table_dict[str(i)]['columns'][str(j.name)] = {}
                table_dict[str(i)]['columns'][str(j.name)]['name'] = j.name
                table_dict[str(i)]['columns'][str(j.name)]['type'] = j.type
                table_dict[str(i)]['columns'][str(j.name)]['primary_key'] = j.primary_key
        # 生成init
        init_list = self.init_codegen(table_dict)
        # 生成urls
        urls_list = self.urls_codegen(table_dict)
        # 生成resource
        resource_list = self.resource_codegen(table_dict)
        # 生成otherResource
        otherResource_list = self.other_resource_codegen(table_dict)

    # 生成init
    def init_codegen(self, tables):
        files = []
        for i in tables:
            # 获得表名
            table_name = str(i)
            # 去除下划线
            api_name = str_format_convert(table_name)

            # 模版生成
            api_str = '{0}_api = Blueprint("{1}", __name__)'.format(api_name.lower(), api_name)
            files.append(self.template_init.format(
                api=api_str))

        # print(files[0])
        return files

    # 生成urls
    def urls_codegen(self, tables):
        files = []
        for i in tables:
            # 获得表名
            table_name = str(i)
            # 去除下划线
            api_name = str_format_convert(table_name)

            # 模版生成
            import_str = """from . import {0}_api
form api_1.{1}Resource.{1}Resource import {2}Resource
from api_1.{1}Resource.{1}OtherResource import {2}OtherResource""".format(
                api_name.lower(), api_name, api_name.capitalize())

            api_str = 'APi({0}_api)'.format(api_name)

            # 获取主键列表
            primary_keys = []
            for j in tables[i].get('columns').values():
                if j.get('primary_key'):
                    primary_keys.append(j.get('name'))

            primary_keys_str = ''
            for i in range(len(primary_keys)):
                primary_keys_str += '/<int:' + str_format_convert(primary_keys[i]) + '>'
            resource_str = 'api.add_resource({0}, {1}, endpoint={2})'.format(
                api_name.capitalize(), primary_keys_str, api_name)

            other_resource_str = 'api.add_resource({0}, '', endpoint={1}_list)'.format(
                api_name.capitalize(), api_name)

            files.append(self.template_urls.format(
                importStr=import_str, api=api_str, resource=resource_str, otherResource=other_resource_str))
            print(files[0])
        return files

    # 生成resource
    def resource_codegen(self, tables):
        files = []
        for i in tables:
            # 获得表名
            table_name = str(i)
            # 去除下划线
            api_name = str_format_convert(table_name)

            # 模版生成
            import_str = """
from controller.{0}Controller import {0}Controller
from service.{0}Service import {0}Service
from utils import commons
from utils.response_code import RET
""".format(api_name)

            className_str = api_name.capitalize()

            # 获取主键列表
            primary_keys = []
            for j in tables[i].get('columns').values():
                if j.get('primary_key'):
                    primary_keys.append(j.get('name'))

            primary_keys_str = ''
            for i in range(len(primary_keys)):
                primary_keys_str += ', ' + primary_keys[i]
            id_str = primary_keys_str

            # 获取字段列表
            fields = []
            argument_str = ''
            for j in tables[i].get('columns').values():
                argument_str += 'parser.add_argument("{0}", type="{1}", location="form", required=False, help="{0}参数类型不正确或缺失")'.format(
                    j.name, mysql_map[j['type']]
                )
        return files

    # 生成otherResource
    def other_resource_codegen(self, tables):
        files = []
        return files
