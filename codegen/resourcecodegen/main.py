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

from codegen import codegen_layer, tables, metadata
from codegen.resourcecodegen.codegenerator import CodeGenerator
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

        if not tables:
            return

        # Get target directory
        new_file_or_dir(2, Settings.TARGET_DIR)
        new_file_or_dir(2, Settings.PROJECT_DIR)
        api_dir = os.path.join(Settings.PROJECT_DIR, 'api_' + Settings.API_VERSION)
        new_file_or_dir(2, api_dir)

        api_init_file = os.path.join(api_dir, '__init__.py')
        file_write(api_init_file, '#!/usr/bin/env python \n# -*- coding:utf-8 -*-')

        app_dir = os.path.join(Settings.PROJECT_DIR, 'app')
        new_file_or_dir(2, app_dir)

        generator = CodeGenerator(metadata)
        generator.resource_generator(api_dir, app_dir)
    except Exception as e:
        loggings.error(1, str(e))
