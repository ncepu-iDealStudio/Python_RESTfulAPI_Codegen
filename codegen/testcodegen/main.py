#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:50
# Author:yuanronghao
# @File:main.py.py
# @Software:PyCharm


import os

from codegen.testcodegen.codegenerator import CodeGenerator
from .template.filetemplate import FileTemplate
from utils.common import file_write
from utils.loggings import loggings
from codegen import project_dir, target_dir


def main(table_dict):
    """
    Generate resource layer code
    :return: None
    """

    try:
        if not list(table_dict.keys()):
            return

        # Get target directory
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(project_dir, exist_ok=True)

        test_dir = os.path.join(project_dir, 'test')
        os.makedirs(test_dir, exist_ok=True)

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
        os.makedirs(report_dir, exist_ok=True)

        generator = CodeGenerator()
        generator.test_generator(test_dir, table_dict)


    except Exception as e:
        loggings.error(1, str(e))
