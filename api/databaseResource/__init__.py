#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2024/1/15 15:09
# software: PyCharm

'''
    this is function  description 
'''
from flask import Blueprint

database_blueprint = Blueprint("database", __name__)

from . import urls
