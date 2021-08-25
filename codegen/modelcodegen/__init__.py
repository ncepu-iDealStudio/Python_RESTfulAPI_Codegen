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

from config.setting import Settings

project_dir = Settings.PROJECT_DIR
# 在目标路径生成models的目录
os.makedirs(models_path := os.path.join(project_dir, 'models'), exist_ok=True)

cmd = "flask-sqlacodegen {url}{schema}{tables}{noviews}{noindexes}" \
      " {noconstraints}{nojoined}{noinflect}{noclasses}{notables}{outfile}{nobackrefs}" \
      " {nocomments}{ignore_cols} --flask"
