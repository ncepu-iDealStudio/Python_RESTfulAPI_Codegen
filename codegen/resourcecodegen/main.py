#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:PigKinght
# datetime:2021/8/26 15:34
# software: PyCharm

"""
    this is function description
"""

# file write
import os

from codegen import project_dir, api_version
from codegen.resourcecodegen.codegenerator import CodeGenerator
from utils.loggings import loggings


def main(table_dict):
    """
    Generate resource layer code
    :return: None
    """

    try:
        if not list(table_dict.keys()):
            return

        # Get target directory
        os.makedirs(api_dir := os.path.join(project_dir, 'api_' + api_version), exist_ok=True)
        os.makedirs(app_dir := os.path.join(project_dir, 'app'), exist_ok=True)

        generator = CodeGenerator()
        generator.resource_generator(api_dir, app_dir, table_dict)
        print(1)

    except Exception as e:
        loggings.error(1, str(e))
