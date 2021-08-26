#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:PigKnight
# datetime:2021/8/21 13:29
# software: PyCharm

"""
    this is function  description
"""

import os

import pkg_resources
from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from utils.checkTable import CheckTable

url = Settings.MODEL_URL
schema = Settings.MODEL_SCHEMA
tables = CheckTable.check_primary_key()
noviews = Settings.MODEL_NOVIEWS
codegenLayer = Settings.CODEGEN_LAYER

# Use reflection to fill in the metadata
engine = create_engine(url)
metadata = MetaData(engine)
metadata.reflect(engine, schema, not noviews, tables)
