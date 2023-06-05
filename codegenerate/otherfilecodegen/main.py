#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:PigKinght
# datetime:2021/8/26 15:34
# software: PyCharm

"""
    this is function description
"""


import os

from codegenerate.otherfilecodegen.codegenerator import CodeGenerator
from utils.loggings import loggings


def generate_other_file_layer(table_dict, settings, session_id, ip):
    """
    Generate resource layer code
    :return: None
    """

    try:
        project_dir = settings.PROJECT_DIR

        os.makedirs(app_dir := os.path.join(project_dir, 'app'), exist_ok=True)

        generator = CodeGenerator(settings, session_id, ip)
        generator.other_file_generator(app_dir, table_dict)
        print(1)

    except Exception as e:
        loggings.error(1, str(e), session_id, ip)
