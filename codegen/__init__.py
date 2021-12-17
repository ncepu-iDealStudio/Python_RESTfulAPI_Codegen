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
from utils.tablesMetadata import TableMetadata

# reload settings
TableMetadata.reload()

# Initialize the parameters for this code generator.
# 为代码生成器初始化参数
url = Settings.MODEL_URL
engine = create_engine(url)
metadata = MetaData(engine)

metadata.reflect(engine, only=Settings.MODEL_TABLES if Settings.MODEL_TABLES else None)

# 代码生成的层次
codegen_layer = 'default'

# 数据库模式
schema = Settings.MODEL_SCHEMA

# 无视图
noviews = Settings.MODEL_NOVIEWS

# 项目路径
project_dir = Settings.PROJECT_DIR

# 目标项目路径
target_dir = Settings.TARGET_DIR

# 数据表信息字典
table_dict = CheckTable.main(metadata)

