#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:29
# software: PyCharm

"""
    this is function  description
"""
import io
import os
import sys

import pkg_resources
from sqlalchemy import create_engine, MetaData
from config.setting import Settings
from codegen.controllercodegen.codegen import CodeGenerator
from utils.checkTable import CheckTable
from utils.common import new_file_or_dir


def controllerGenerate():
    """
    生成Controller层代码
    :return: None
    """
    url = Settings.MODEL_URL
    codegen_layer = Settings.CODEGEN_LAYER
    schema = Settings.MODEL_SCHEMA
    version = Settings.MODEL_VERSION
    noviews = Settings.MODEL_NOVIEWS
    record_delete_way = Settings.CONTROLLER_RECORD_DELETE_WAY

    # 代码生成层级不为默认或控制器，直接返回
    if codegen_layer not in ['default', 'controller']:
        return

    if version:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return

    tables = CheckTable.check_primary_key()
    if tables is None:
        return

    # 获取目标目录
    new_file_or_dir(2, Settings.TARGET_DIR)
    new_file_or_dir(2, Settings.PROJECT_DIR)
    controller_dir = os.path.join(Settings.PROJECT_DIR, 'controller')
    new_file_or_dir(2, controller_dir)

    # 连接数据库用反射获取元数据
    engine = create_engine(url)
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, not noviews, tables)

    generator = CodeGenerator(metadata)
    generator.controller_codegen(delete_way=record_delete_way, controller_dir=controller_dir)
    return True

