#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/20 15:59
# software: PyCharm

"""
    load public settings and Initialize the parameters
"""

from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from utils.checkTable import CheckTable

# Initialize the parameters for this code generator.
# 为代码生成器初始化参数
url = Settings.MODEL_URL
codegen_layer = Settings.CODEGEN_LAYER
schema = Settings.MODEL_SCHEMA
noviews = Settings.MODEL_NOVIEWS
tables = CheckTable.check_primary_key()
project_dir = Settings.PROJECT_DIR
target_dir = Settings.TARGET_DIR

# link to the database and get metadata by reflection
engine = create_engine(url)
metadata = MetaData(engine)
metadata.reflect(engine, schema, not noviews, tables)
