#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:29
# software: PyCharm
'''
    this is function  description 
'''
import io
import sys

import pkg_resources
from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from codegen.resourcecodegen.codegen import CodeGenerator


def resourceGenerate():
    """
    生成Resource层代码层代码
    :return: None
    """
    return
    url = Settings.MODEL_URL
    version = Settings.MODEL_VERSION
    schema = Settings.MODEL_SCHEMA
    tables = Settings.MODEL_TABLES
    noviews = Settings.MODEL_NOVIEWS
    # noindexes = Settings.MODEL_NOINDEXES
    # noconstraints = Settings.MODEL_NOCONSTRAINTS
    # nojoined = Settings.MODEL_NOJOINED
    # noinflect = Settings.MODEL_NOINFLECT
    # noclasses = Settings.MODEL_NOCLASSES
    # nocomments = Settings.MODEL_NOCOMMENTS
    outfile = Settings.MODEL_OUTFILE

    if version:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return

    if not url:
        print('You must supply a url\n', file=sys.stderr)
        return

        # Use reflection to fill in the metadata
    engine = create_engine(url)
    metadata = MetaData(engine)
    tables = tables.split(',') if tables else None

    # tables = None
    tables = ['order']
    if tables:
        metadata.reflect(engine, schema, not noviews, tables)
    else:
        metadata.reflect(engine, schema, not noviews, None)
    # Write the generated model code to the specified file or standard output
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.resource_generator(outfile)
    return
