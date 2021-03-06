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

from utils.common import str_to_little_camel_case
from utils.loggings import loggings
from . import cmd


def main(table_dict, settings, session_id, ip):
    """
    model层代码的生成
    :return: None
    """

    try:
        project_dir = settings.PROJECT_DIR
        model_url = settings.MODEL_URL

        # 在项目文件夹中创建models的目录
        models_path = os.path.join(project_dir, 'models')
        os.makedirs(models_path, exist_ok=True)

        # 创建空的 __init__.py 文件
        with open(os.path.join(models_path, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python\n# -*- coding:utf-8 -*-\n")

        tables = list(table_dict.keys())

        # 为每张表生成model层代码
        for table in tables:
            loggings.info(1, "Model code for {0} table is being generated".format(table), session_id, ip)
            command = cmd.format(
                url=model_url,
                schema="",
                tables=" --tables {0}".format(table),
                noviews="",
                noindexes="",
                noconstraints="",
                nojoined="",
                noinflect="",
                noclasses="",
                notables="",
                outfile=" --outfile {0}/{1}".format(models_path, str_to_little_camel_case(table) + "Model.py"),
                nobackrefs="",
                nocomments="",
                ignore_cols=""
            )
            os.system(command)

    except Exception as e:
        loggings.exception(1, e, session_id, ip)
