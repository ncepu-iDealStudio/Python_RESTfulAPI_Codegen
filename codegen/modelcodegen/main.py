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

from codegen import project_dir, tables
from config.setting import Settings
from utils.common import str_format_convert
from utils.loggings import loggings
from . import cmd


def modelGenerate():
    """
    model层代码的生成
    :return: None
    """

    try:

        # 在项目文件夹中创建models的目录
        os.makedirs(models_path := os.path.join(project_dir, 'models'), exist_ok=True)

        with open(os.path.join(models_path, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python\n# -*- coding:utf-8 -*-\n")

        for table in tables:
            loggings.info(1, "Model code for {0} table is being generated".format(table))
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
