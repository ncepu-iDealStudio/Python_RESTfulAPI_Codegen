#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:PigKnight
# datetime:2021/8/21 13:29
# software: PyCharm

"""
    this is function  description 
"""

import os

import pkg_resources
from sqlalchemy import create_engine, MetaData

from codegen.resourcecodegen.codegenerator import CodeGenerator
from config.setting import Settings
from utils.checkTable import CheckTable
from utils.common import new_file_or_dir
from utils.loggings import loggings


def resourceGenerate():
    """
    Generate resource layer code
    :return: None
    """
    try:
        # return
        url = Settings.MODEL_URL
        version = Settings.MODEL_VERSION
        schema = Settings.MODEL_SCHEMA
        tables = CheckTable.check_primary_key()
        noviews = Settings.MODEL_NOVIEWS
        codegenLayer = Settings.CODEGEN_LAYER

        #  It returns directly if the code generation level is not the 'default' or 'controller
        if codegenLayer not in ['default', 'controller']:
            return

        if version:
            version = pkg_resources.get_distribution('sqlacodegen').parsed_version
            print(version.public)
            return

        # Get target directory
        new_file_or_dir(2, Settings.TARGET_DIR)
        new_file_or_dir(2, Settings.PROJECT_DIR)
        api_dir = os.path.join(Settings.PROJECT_DIR, 'api_'+Settings.API_VERSION)
        new_file_or_dir(2, api_dir)
        app_dir = os.path.join(Settings.PROJECT_DIR, 'app')
        new_file_or_dir(2, app_dir)

        # Use reflection to fill in the metadata
        engine = create_engine(url)
        metadata = MetaData(engine)

        metadata.reflect(engine, schema, not noviews, tables)
        generator = CodeGenerator(metadata)
        generator.resource_generator(api_dir, app_dir)
        return
    except Exception as e:
        loggings.error(1, str(e))
