#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:50
# Author:yuanronghao
# @File:main.py.py
# @Software:PyCharm


import os

from code_generate.testcodegen.codegenerator import CodeGenerator
from .template.filetemplate import FileTemplate
from utils.loggings import loggings


def generate_test_layer(table_dict, settings, session_id, ip):
    """
    Generate resource layer code
    :return: None
    """
    project_dir = settings.PROJECT_DIR
    target_dir = settings.TARGET_DIR

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
        # file_write(test_init_dir, FileTemplate.test_init)
        with open(test_init_dir, 'w', encoding='utf8') as f:
            f.write(FileTemplate.test_init)

        # pytest ini file generation
        pytestini_dir = os.path.join(test_dir, 'pytest.ini')
        # file_write(pytestini_dir, FileTemplate.pytest_ini)
        with open(pytestini_dir, 'w', encoding='utf8') as f:
            f.write(FileTemplate.pytest_ini)
        # test start file generation
        test_start_dir = os.path.join(test_dir, 'test_start.py')
        # file_write(test_start_dir, FileTemplate.test_start)
        with open(test_start_dir, 'w', encoding='utf8') as f:
            f.write(FileTemplate.test_start)
        # report dir generation
        report_dir = os.path.join(test_dir, 'report')
        os.makedirs(report_dir, exist_ok=True)

        generator = CodeGenerator()
        generator.test_generator(test_dir, table_dict, session_id, ip)

    except Exception as e:
        loggings.error(1, str(e), session_id, ip)
