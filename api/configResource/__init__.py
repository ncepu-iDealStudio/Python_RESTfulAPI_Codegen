#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2024/1/15 15:57
# software: PyCharm

'''
    this is function  description 
'''
from flask import Blueprint

config_blueprint = Blueprint("config", __name__)

from . import urls

