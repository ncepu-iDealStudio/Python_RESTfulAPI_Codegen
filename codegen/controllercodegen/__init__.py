#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:29
# software: PyCharm

"""
    this is function  description
"""
import os

import pkg_resources
from sqlalchemy import create_engine, MetaData

from codegen.controllercodegen.codegen import CodeGenerator
from config.setting import Settings
from utils.checkTable import CheckTable
from utils.common import new_file_or_dir


def controllerGenerate():
    """
    Generate Controller code
    :return: None
    """
    url = Settings.MODEL_URL
    codegen_layer = Settings.CODEGEN_LAYER
    schema = Settings.MODEL_SCHEMA
    version = Settings.MODEL_VERSION
    noviews = Settings.MODEL_NOVIEWS
    record_delete_way = Settings.CONTROLLER_RECORD_DELETE_WAY

    # return, while codegen_layer is not 'default' or 'controller'
    if codegen_layer not in ['default', 'controller']:
        return

    if version:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return

    tables = CheckTable.check_primary_key()
    if tables is None:
        return

    # get the target dir
    new_file_or_dir(2, Settings.TARGET_DIR)
    new_file_or_dir(2, Settings.PROJECT_DIR)
    controller_dir = os.path.join(Settings.PROJECT_DIR, 'controller')
    new_file_or_dir(2, controller_dir)

    # link to the database and get metadata by reflection
    engine = create_engine(url)
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, not noviews, tables)

    generator = CodeGenerator(metadata)
    generator.controller_codegen(delete_way=record_delete_way, controller_dir=controller_dir)
    return

