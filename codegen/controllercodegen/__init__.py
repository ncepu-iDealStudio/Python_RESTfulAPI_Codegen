#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:29
# software: PyCharm

"""
    load settings and init
"""
from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from utils.checkTable import CheckTable

url = Settings.MODEL_URL
codegen_layer = Settings.CODEGEN_LAYER
schema = Settings.MODEL_SCHEMA
noviews = Settings.MODEL_NOVIEWS
record_delete_way = Settings.CONTROLLER_RECORD_DELETE_WAY
tables = CheckTable.check_primary_key()

# link to the database and get metadata by reflection
engine = create_engine(url)
metadata = MetaData(engine)
metadata.reflect(engine, schema, not noviews, tables)
