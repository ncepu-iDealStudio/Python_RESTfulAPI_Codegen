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
from utils.checkTable import CheckTable

project_dir = Settings.PROJECT_DIR
# 在项目文件夹中创建models的目录
os.makedirs(models_path := os.path.join(project_dir, 'models'), exist_ok=True)

with open(os.path.join(models_path, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write("#!/usr/bin/env python\n# -*- coding:utf-8 -*-\n")

cmd = "flask-sqlacodegen {url}{schema}{tables}{noviews}{noindexes}" \
      " {noconstraints}{nojoined}{noinflect}{noclasses}{notables}{outfile}{nobackrefs}" \
      " {nocomments}{ignore_cols} --flask"

tables = CheckTable.check_primary_key()