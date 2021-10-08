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

from codegen import table_dict
from codegen.testcodegen.template.filetemplate import FileTemplate
from config.setting import Settings
from utils.common import str_format_convert, new_file_or_dir, file_write
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self):
        super(CodeGenerator, self).__init__()

    # testcode generator
    def test_generator(self, test_dir):
        # reload settings
        Settings.reload()

        try:

            # test generation
            loggings.info(1, 'Start generating Test layer, please wait...')

            # Test_Controller generation
            loggings.info(1, 'Start generating TestController layer, please wait...')

            # Test_Controller dir generation
            TestController_dir = os.path.join(test_dir, 'Test_Controller')
            new_file_or_dir(2, TestController_dir)
            init_file = os.path.join(TestController_dir, '__init__.py')
            init_list = self.init_codegen()
            file_write(init_file, init_list)

            # Test_xController generation
            for table in table_dict.keys():
                tableName = str_format_convert(table_dict[table].get('table_name'))

                test_xController_dir = os.path.join(test_dir, TestController_dir,
                                                    'Test_{0}Controller'.format(tableName))
                new_file_or_dir(2, test_xController_dir)

                # init generation
                init_file = os.path.join(test_xController_dir, '__init__.py')
                init_list = self.init_codegen()

                # datas.py generation
                datas_file = os.path.join(test_xController_dir, 'datas.py')
                datas_list = self.controller_datas_codegen()

                # test_xController generation
                test_controller_file = os.path.join(test_xController_dir,
                                                    'test_{0}Controller.py'.format(tableName))
                test_controller_list = self.controllertest_codegen(tableName,
                                                                   tableName[0].upper() + tableName[1:])

                # file write
                loggings.info(1, 'Generating {0}'.format('Test_{0}Controller'.format(tableName)))
                file_write(init_file, init_list)
                file_write(datas_file, datas_list)
                file_write(test_controller_file, test_controller_list)

            loggings.info(1, 'Generating TestController layer complete')

            # Test_Controller generation
            loggings.info(1, 'Start generating TestResource layer, please wait...')

            # Test_Resource dir generation
            TestResource_dir = os.path.join(test_dir, 'Test_Resource')
            new_file_or_dir(2, TestResource_dir)

            # Test_Resource init generation
            init_file = os.path.join(TestResource_dir, '__init__.py')
            init_list = self.init_codegen()
            file_write(init_file, init_list)

            # Test_Resource  utils  generation
            utils_file = os.path.join(TestResource_dir, 'utils.py')
            utils_list = self.resource_utils_codegen()
            file_write(utils_file, utils_list)

            # Test_xResource generation
            for table in table_dict.keys():
                tableName = str_format_convert(table_dict[table].get('table_name'))

                test_xResource_dir = os.path.join(test_dir, TestResource_dir,
                                                  'Test_{0}Resource'.format(tableName))
                new_file_or_dir(2, test_xResource_dir)

                # init generation
                init_file = os.path.join(test_xResource_dir, '__init__.py')
                init_list = self.init_codegen()

                # datas.py generation
                datas_file = os.path.join(test_xResource_dir, 'datas.py')
                datas_list = self.resource_datas_codegen()

                # test_xResource generation
                test_rescource_file = os.path.join(test_xResource_dir,
                                                   'test_{0}Controller.py'.format(tableName))
                test_rescource_list = self.resourcetest_codegen(tableName)

                # file write
                loggings.info(1, 'Generating {0}'.format('Test_{0}Controller'.format(tableName)))
                file_write(init_file, init_list)
                file_write(datas_file, datas_list)
                file_write(test_rescource_file, test_rescource_list)

            loggings.info(1, 'Generating TestResource layer complete')

            loggings.info(1, 'Generating Test layer complete')
        except Exception as e:
            loggings.exception(1, e)
            return
        pass

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
