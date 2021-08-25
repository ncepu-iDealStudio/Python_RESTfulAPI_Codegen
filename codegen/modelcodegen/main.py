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

from codegen.modelcodegen import cmd, models_path
from config.setting import Settings
from utils.checkTable import CheckTable
from utils.loggings import loggings
from utils.common import str_format_convert


def modelGenerate():
    """
    model层代码的生成
    :return: None
    """

    tables = CheckTable.check_primary_key()

    try:
        for table in tables:
            loggings.info(1, "正在生成{0}表的model代码".format(table))
            command = cmd.format(
                url=Settings.MODEL_URL,
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
            os.system(command)
    except Exception as e:
        loggings.error(1, str(e))
