#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:jackiex
# datetime:2021/8/21 13:32
# software: PyCharm

'''
    功能说明：将目标项目所需要的静态配置资源同步至项目下
'''

import os

from utils.common import new_file_or_dir
from .main import copy_static
from config.setting import Settings


def staticGenerate():
    """
     同步静态文件
    :return: 静态资源拷贝完成状态
    """
    # 获取目标目录
    new_file_or_dir(2, Settings.TARGET_DIR)
    new_file_or_dir(2, Settings.PROJECT_DIR)

    # 获取静态资源目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_dir = os.path.join(BASE_DIR,  'static')
    return copy_static(Settings.PROJECT_DIR, source_dir)

