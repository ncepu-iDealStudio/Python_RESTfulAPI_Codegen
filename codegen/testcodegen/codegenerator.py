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

from codegen.testcodegen.template.filetemplate import FileTemplate
from utils.common import str_format_convert
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self):
        super(CodeGenerator, self).__init__()

    # testcode generator
    def test_generator(self, test_dir, table_dict):
        # reload settings
        # Settings.reload()

        try:

            # test generation
            loggings.info(1, 'Start generating Test layer, please wait...')

            # Test_Controller generation
            loggings.info(1, 'Start generating TestController layer, please wait...')

            # Test_Controller dir generation
            os.makedirs(TestController_dir := os.path.join(test_dir, 'Test_Controller'), exist_ok=True)
            with open(os.path.join(TestController_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(self.init_codegen())

            # Test_xController generation
            for table in table_dict.keys():
                if table_dict[table]['is_view']:
                    continue
                tableName = str_format_convert(table_dict[table].get('table_name'))
                os.makedirs(test_xController_dir := os.path.join(test_dir, TestController_dir,
                                                                 'Test_{0}Controller'.format(tableName)), exist_ok=True)

                # init generation
                with open(os.path.join(test_xController_dir, '__init__.py'), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen())

                # datas.py generation
                with open(os.path.join(test_xController_dir, 'datas.py'), 'w', encoding='utf8') as f:
                    f.write(self.controller_datas_codegen())

                # test_xController generation
                with open(os.path.join(test_xController_dir, 'test_{0}Controller.py'.format(tableName)), 'w',
                          encoding='utf8') as f:
                    f.write(self.controllertest_codegen(tableName,
                                                        tableName[0].upper() + tableName[1:]))

                # file write
                loggings.info(1, 'Generating {0}'.format('Test_{0}Controller'.format(tableName)))

            loggings.info(1, 'Generating TestController layer complete')

            # Test_Controller generation
            loggings.info(1, 'Start generating TestResource layer, please wait...')

            # Test_Resource dir generation
            os.makedirs(TestResource_dir := os.path.join(test_dir, 'Test_Resource'), exist_ok=True)

            # Test_Resource init generation
            with open(os.path.join(TestResource_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(self.init_codegen())

            # Test_Resource  utils  generation
            with open(os.path.join(TestResource_dir, 'utils.py'), 'w', encoding='utf8') as f:
                f.write(self.resource_utils_codegen())

            # Test_xResource generation
            for table in table_dict.keys():
                if table_dict[table]['is_view']:
                    continue
                tableName = str_format_convert(table_dict[table].get('table_name'))

                os.makedirs(test_xResource_dir := os.path.join(test_dir, TestResource_dir,
                                                               'Test_{0}Resource'.format(tableName)), exist_ok=True)

                # init generation
                with open(os.path.join(test_xResource_dir, '__init__.py'), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen())

                # datas.py generation
                with open(os.path.join(test_xResource_dir, 'datas.py'), 'w', encoding='utf8') as f:
                    f.write(self.resource_datas_codegen())

                # test_xResource generation
                with open(os.path.join(test_xResource_dir, 'test_{0}Resource.py'.format(tableName)), 'w',
                          encoding='utf8') as f:
                    f.write(self.resourcetest_codegen(tableName))

                # file write
                loggings.info(1, 'Generating {0}'.format('Test_{0}Resource'.format(tableName)))

            loggings.info(1, 'Generating TestResource layer complete')

            loggings.info(1, 'Generating Test layer complete')

        except Exception as e:
            loggings.exception(1, e)
            return

    # init generation
    def init_codegen(self):
        return FileTemplate.init

    # test init generation
    def test_init_codegen(self):
        return FileTemplate.test_init

    # pytest_ini generation
    def pytest_ini_codegen(self):
        return FileTemplate.pytest_ini

    # test_start generation
    def teststart_codegen(self):
        return FileTemplate.test_start

    # conrtoller

    # controller testcode generation
    def controller_init_codegen(self):
        return FileTemplate.init

    # controllertest_init generation
    def controllertest_init_codegen(self):
        return FileTemplate.init

    # controllertest generation
    def controllertest_codegen(self, controllerName_str, controllerClassName_str):
        return FileTemplate.test_controller.format(
            controllerName=controllerName_str,
            controllerClassName=controllerClassName_str
        )

    #  controller_datas generation
    def controller_datas_codegen(self):
        return FileTemplate.controller_datas

    # resource

    #  generation
    def resourcetest_codegen(self, resourceName_str):
        return FileTemplate.test_resource.format(
            resourceName=resourceName_str
        )

    # resource_init generation
    def resource_init_codegen(self):
        return FileTemplate.init

    #  generation
    def resourcetest_init_codegen(self):
        return FileTemplate.init

    #  generation
    def resource_datas_codegen(self):
        return FileTemplate.resource_datas

    def resource_utils_codegen(self):
        return FileTemplate.test_resource_utils
