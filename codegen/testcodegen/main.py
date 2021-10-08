#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:50
# Author:yuanronghao
# @File:main.py.py
# @Software:PyCharm


# file write
import os

from codegen import codegen_layer, table_dict
from codegen.testcodegen.codegenerator import CodeGenerator
from .template.filetemplate import FileTemplate
from config.setting import Settings
from utils.common import new_file_or_dir, file_write
from utils.loggings import loggings


def main():
    """
    Generate resource layer code
    :return: None
    """
    try:
        #  It returns directly if the code generation level is not the 'default' or 'resource'
        if codegen_layer not in ['default', 'resource']:
            return

        if not list(table_dict.keys()):
            return

        # Get target directory
        new_file_or_dir(2, Settings.TARGET_DIR)
        new_file_or_dir(2, Settings.PROJECT_DIR)
        test_dir = os.path.join(Settings.PROJECT_DIR, 'test')
        new_file_or_dir(2, test_dir)

        # test init file generation
        test_init_dir = os.path.join(test_dir, '__init__.py')
        file_write(test_init_dir, FileTemplate.test_init)
        # pytest ini file generation
        pytestini_dir = os.path.join(test_dir, 'pytest.ini')
        file_write(pytestini_dir, FileTemplate.pytest_ini)

        # test start file generation
        test_start_dir = os.path.join(test_dir, 'test_start.py')
        file_write(test_start_dir, FileTemplate.test_start)

        # report dir generation
        report_dir = os.path.join(test_dir, 'report')
        new_file_or_dir(2, report_dir)

        generator = CodeGenerator()
        generator.test_generator(test_dir)
    except Exception as e:
        loggings.error(1, str(e))
