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

from codegen.resourcecodegen.codegenerator import CodeGenerator
from config.setting import Settings
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
        os.makedirs(api_dir := os.path.join(Settings.PROJECT_DIR, 'api_' + Settings.API_VERSION), exist_ok=True)
        os.makedirs(app_dir := os.path.join(Settings.PROJECT_DIR, 'app'), exist_ok=True)

        generator = CodeGenerator()
        generator.resource_generator(api_dir, app_dir)

    except Exception as e:
        loggings.error(1, str(e))
