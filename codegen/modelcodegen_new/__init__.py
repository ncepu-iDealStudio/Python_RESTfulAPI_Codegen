#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/25 11:12
# software: PyCharm

"""
    this is function description
"""

import os
import sys

from config.setting import Settings
from utils.checkTable import CheckTable
from utils.loggings import loggings
from utils.common import str_format_convert

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version


def modelGenerate():
    """
    model层代码的生成
    :return: None
    """
    url = Settings.MODEL_URL
    sqlacodegen_version = Settings.MODEL_VERSION
    codegen_mode = Settings.CODEGEN_MODE
    project_dir = Settings.PROJECT_DIR

    if sqlacodegen_version:
        print(version('sqlacodegen'))
        return
    if not url:
        loggings.error(1, 'You must supply a url!')
        return

    # 判断代码生成模式-database|table-整库模式|多表模式
    if codegen_mode == 'database':
        tables = CheckTable.check_primary_key()

    elif codegen_mode == "table":
        tables = Settings.MODEL_TABLES.split(',') if Settings.MODEL_TABLES else None
        # Preprocessing -- remove the spaces on both sides of the table name
        for index in range(len(tables)):
            tables[index] = tables[index].strip()

    try:
        # 在目标路径生成models的目录
        os.makedirs(models_path := os.path.join(project_dir, 'models'), exist_ok=True)

        for table in tables:
            cmd = "flask-sqlacodegen {url}{schema}{tables}{noviews}{noindexes}" \
                  " {noconstraints}{nojoined}{noinflect}{noclasses}{notables}{outfile}{nobackrefs}" \
                  " {nocomments}{ignore_cols} --flask"
            cmd = cmd.format(
                url=url,
                schema="",
                tables=" --tables {0}".format(table),
                noviews="",
                noindexes="",
                noconstraints="",
                nojoined="",
                noinflect="",
                noclasses="",
                notables="",
                outfile=" --outfile {0}\{1}".format(models_path, str_format_convert(table) + "Model.py"),
                nobackrefs="",
                nocomments="",
                ignore_cols=""
            )
            os.system(cmd)
    except Exception as e:
        loggings.error(1, str(e))
