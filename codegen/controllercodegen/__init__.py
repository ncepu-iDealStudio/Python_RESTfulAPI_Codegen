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
import sys

from sqlalchemy import create_engine, MetaData
from config.setting import Settings
from codegen.controllercodegen.codegen import CodeGenerator


def controllerGenerate():
    """
    生成Controller层代码
    :return: None
    """
    url = Settings.MODEL_URL
    codegen_mode = Settings.CODEGEN_MODE
    codegen_layer = Settings.CODEGEN_LAYER
    schema = Settings.MODEL_SCHEMA
    version = Settings.MODEL_VERSION
    tables = Settings.MODEL_TABLES
    noviews = Settings.MODEL_NOVIEWS
    noindexes = Settings.MODEL_NOINDEXES
    noconstraints = Settings.MODEL_NOCONSTRAINTS
    nojoined = Settings.MODEL_NOJOINED
    noinflect = Settings.MODEL_NOINFLECT
    noclasses = Settings.MODEL_NOCLASSES
    nocomments = Settings.MODEL_NOCOMMENTS
    outfile = Settings.MODEL_OUTFILE
    record_delete_way = Settings.CONTROLLER_RECORD_DELETE_WAY

    # 代码生成层级不为默认或控制器，直接返回
    if codegen_layer not in ['default', 'controller']:
        return

    # 连接数据库用反射获取元数据
    engine = create_engine(url)
    metadata = MetaData(engine)
    if codegen_mode == 'database':
        metadata.reflect(engine, schema, not noviews)
    else:
        tables = tables.split(',')
        metadata.reflect(engine, schema, not noviews, tables)

    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.controller_codegen(outfile)

