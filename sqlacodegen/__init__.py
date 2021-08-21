#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/20 15:59
# software: PyCharm

from __future__ import unicode_literals, division, print_function, absolute_import

import io
import sys

import pkg_resources
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from config.setting import Settings
from sqlacodegen.modelcodegen.codegen import CodeGenerator


def modelGenerate():
    """
    model层代码的生成
    :return: None
    """
    url = Settings.MODEL_URL
    version = Settings.MODEL_VERSION
    schema = Settings.MODEL_SCHEMA
    tables = Settings.MODEL_TABLES
    noviews = Settings.MODEL_NOVIEWS
    noindexes = Settings.MODEL_NOINDEXES
    noconstraints = Settings.MODEL_NOCONSTRAINTS
    nojoined = Settings.MODEL_NOJOINED
    noinflect = Settings.MODEL_NOINFLECT
    noclasses = Settings.MODEL_NOCLASSES
    nocomments = Settings.MODEL_NOCOMMENTS
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

    metadata.reflect(engine, schema, not noviews, tables)

    # Write the generated model code to the specified file or standard output
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata, noindexes, noconstraints, nojoined,
                              noinflect, noclasses, nocomments=nocomments)
    generator.render(outfile)
    return


def controllerGenerate():
    """
    生成Controller层代码
    :return: None
    """
    pass


def resourceGenerate():
    """
    生成Resource层代码层代码
    :return: None
    """
    pass


def staticGenerate():
    """
    打包静态文件
    :return: None
    """
    pass
