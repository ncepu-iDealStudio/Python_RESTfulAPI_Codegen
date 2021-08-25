#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:29
# software: PyCharm
'''
    this is function  description 
'''
import os
import sys

import pkg_resources
from sqlalchemy import create_engine, MetaData

from codegen.resourcecodegen.codegenrator import CodeGenerator
from config.setting import Settings
from utils.checkTable import CheckTable
from utils.common import new_file_or_dir


def resourceGenerate():
    """
    生成Resource层代码层代码
    :return: None
    """
    # return
    url = Settings.MODEL_URL
    version = Settings.MODEL_VERSION
    schema = Settings.MODEL_SCHEMA
    tables = CheckTable.check_primary_key()
    noviews = Settings.MODEL_NOVIEWS

    if version:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return

    if not url:
        print('You must supply a url\n', file=sys.stderr)
        return

    # 获取目标目录
    new_file_or_dir(2, Settings.TARGET_DIR)
    new_file_or_dir(2, Settings.PROJECT_DIR)
    api_dir = os.path.join(Settings.PROJECT_DIR, 'api_1')
    new_file_or_dir(2, api_dir)

    # Use reflection to fill in the metadata
    engine = create_engine(url)
    metadata = MetaData(engine)

    metadata.reflect(engine, schema, not noviews, tables)
    generator = CodeGenerator(metadata)
    generator.resource_generator(api_dir)
    return
