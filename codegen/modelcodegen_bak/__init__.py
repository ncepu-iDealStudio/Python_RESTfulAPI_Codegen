#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py
# author:Nathan
# datetime:2021/8/21 11:47
# software: PyCharm

"""
    this is function description
"""

import io
import os
import sys

import pkg_resources
from loguru import logger
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from codegen.modelcodegen_bak.codegen import CodeGenerator
from config.setting import Settings
from utils.loggings import loggings


@logger.catch
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
    codegen_mode = Settings.CODEGEN_MODE

    engine = create_engine(url)
    metadata = MetaData(engine)
    # metadata.reflect(engine)

    if version:
        version = pkg_resources.get_distribution('codegen').parsed_version
        print(version.public)
        return

    if not url:
        loggings.error(1, 'You must supply a url!')
        return

    # Judge the generated code mode -- database or table
    if codegen_mode == 'database1':
        pass
    elif codegen_mode == 'database':
        tables = tables.split(',') if tables else None

        # Preprocessing -- remove the spaces on both sides of the table name
        for index in range(len(tables)):
            tables[index] = tables[index].strip()

        # Use reflection to fill in the metadata
        metadata.reflect(engine, schema, not noviews, tables)

        # Write the generated model code to the specified file or standard output
        os.makedirs(base_path := os.path.join(Settings.TARGET_DIR, Settings.PROJECT_NAME, 'models'), exist_ok=True)
        file_path = os.path.join(base_path, outfile)

        outfile = io.open(file_path, 'w', encoding='utf-8') if outfile else sys.stdout
        generator = CodeGenerator(metadata, noindexes, noconstraints, nojoined,
                                  noinflect, noclasses, nocomments=nocomments)
        generator.render(outfile)
    return
