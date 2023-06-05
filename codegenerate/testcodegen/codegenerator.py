#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:51
# Author:yuanronghao
# @File:codegenerator.py
# @Software:PyCharm
"""
   generate test layer code.
"""

import os

from codegenerate.testcodegen.core.data_template import DataTemplate
from codegenerate.testcodegen.core.filetemplate import FileTemplate
from utils.common import str_format_convert
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self):
        super(CodeGenerator, self).__init__()

    # testcode generator
    def test_generator(self, test_dir, table_dict, session_id, ip):
        # reload settings
        # Settings.reload()
        init_filename = '__init__.py'

        try:

            # test generation
            loggings.info(1, 'Start generating Test layer, please wait...', session_id, ip)

            # Test_Controller generation
            loggings.info(1, 'Start generating test_api_1_0 layer, please wait...', session_id, ip)

            # test_api_1_0 dir generation
            os.makedirs(TestResource_dir := (os.path.join(test_dir, 'test_api_1_0')), exist_ok=True)
            with open(os.path.join(TestResource_dir, init_filename), 'w', encoding='utf8') as f:
                f.write(self.init_codegen())

            # Test_xController generation
            for table in table_dict.keys():
                if table_dict[table]['is_view']:
                    continue
                table_name = str_format_convert(table_dict[table].get('table_name'))
                columns = table_dict[table].get("columns")
                data = "\n"
                for column in columns.values():
                    data = data + "{}{}: {}\n".format(' ' * 6, column['name'], '')

                resource_dir = os.path.join(test_dir, TestResource_dir, '{0}Resource'.format(table_name))
                os.makedirs(resource_dir, exist_ok=True)
                with open(os.path.join(resource_dir, "test_{}Resource.py".format(table_name)), 'w',
                          encoding='utf8') as f:
                    f.write(FileTemplate.test_resource.format(table_name=table_name[0].upper() + table_name[1:]))

                data_dir = os.path.join(resource_dir, "data")
                os.makedirs(data_dir, exist_ok=True)
                with open(os.path.join(data_dir, init_filename), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen())
                with open(os.path.join(data_dir, "delete.yaml"), 'w', encoding='utf8') as f:
                    f.write(DataTemplate.delete_yaml.format(table_name=table_name, data=data))
                with open(os.path.join(data_dir, "get.yaml"), 'w', encoding='utf8') as f:
                    f.write(DataTemplate.get_yaml.format(table_name=table_name))
                with open(os.path.join(data_dir, "post.yaml"), 'w', encoding='utf8') as f:
                    f.write(DataTemplate.post_yaml.format(table_name=table_name, data=data))
                with open(os.path.join(data_dir, "put.yaml"), 'w', encoding='utf8') as f:
                    f.write(DataTemplate.put_yaml.format(table_name=table_name, data=data))

                # file write
                loggings.info(1, 'Generating {0}'.format('{0}Resource'.format(table_name)), session_id, ip)

            loggings.info(1, 'Generating test_api_1_0 layer complete', session_id, ip)

            # Test_xService generation
            loggings.info(1, 'Start generating TestService layer, please wait...', session_id, ip)

            # test_service dir generation
            os.makedirs(test_service_dir := (os.path.join(test_dir, 'test_service')), exist_ok=True)
            with open(os.path.join(TestResource_dir, init_filename), 'w', encoding='utf8') as f:
                f.write(self.init_codegen())

            # xService generation
            for table in table_dict.keys():
                table_name = str_format_convert(table_dict[table].get('table_name'))
                columns = table_dict[table].get("columns")
                data = "\n"
                # print(type(columns))
                if isinstance(columns,dict):
                    for column in columns.values():
                        data = data + "{}{}: {}\n".format(' ' * 6, column['name'], '')
                elif  isinstance(columns,list):
                    for column in columns:
                        data = data + "{}{}: {}\n".format(' ' * 6, column['field_name'], '')

                resource_dir = os.path.join(test_dir, test_service_dir, '{0}Service'.format(table_name))
                os.makedirs(resource_dir, exist_ok=True)
                with open(os.path.join(resource_dir, "test_{}Service.py".format(table_name)), 'w',
                          encoding='utf8') as f:
                    f.write(FileTemplate.test_service.format(table_name=table_name[0].upper() + table_name[1:]))

                with open(os.path.join(resource_dir, init_filename), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen())
                with open(os.path.join(resource_dir, "data.yaml"), 'w', encoding='utf8') as f:
                    f.write(DataTemplate.service_yaml.format(table_name=table_name, data=data))

                loggings.info(1, 'Generating {0}'.format('test_{0}Service'.format(table_name)), session_id, ip)

            loggings.info(1, 'Generating TestService layer complete', session_id, ip)

            loggings.info(1, 'Generating Test layer complete', session_id, ip)

        except Exception as e:
            loggings.exception(1, e, session_id, ip)
            return

    # init generation
    def init_codegen(self):
        return FileTemplate.init

    def env_codegen(self):
        return FileTemplate.env
