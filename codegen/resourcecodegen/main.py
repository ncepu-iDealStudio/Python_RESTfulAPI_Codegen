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
from utils.loggings import loggings


def main(table_dict, settings, session_id, ip):
    """
    Generate resource layer code
    :return: None
    """

    try:
        project_dir = settings.PROJECT_DIR
        api_version = settings.API_VERSION

        os.makedirs(api_dir := os.path.join(project_dir, 'api_' + api_version), exist_ok=True)
        os.makedirs(app_dir := os.path.join(project_dir, 'app'), exist_ok=True)

        generator = CodeGenerator(settings, session_id, ip)
        generator.resource_generator(api_dir, app_dir, table_dict)
        print(1)

    except Exception as e:
        loggings.error(1, str(e), session_id, ip)
