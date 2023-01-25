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

from utils.loggings import loggings
from . import cmd


def generate_model_layer(table_dict, settings, session_id, ip):
    """
    model层代码的生成
    :return: None
    """

    try:
        project_dir = settings.PROJECT_DIR
        model_url = settings.MODEL_URL

        tables = list(table_dict.keys())

        command = cmd.format(
            url=model_url,
            schema="",
            tables=" --tables {0}".format(",".join(tables)),
            noviews="",
            noindexes="",
            noconstraints="",
            nojoined="",
            noinflect="",
            noclasses="",
            notables="",
            outdir=" --outdir {0}".format(project_dir),
            nobackrefs="",
            nocomments="",
            ignore_cols=""
        )

        os.system(command)

        # 为每张表生成model层代码
        for table in tables:
            loggings.info(1, "Model code for {0} table is being generated".format(table), session_id, ip)

    except Exception as e:
        loggings.exception(1, e, session_id, ip)
