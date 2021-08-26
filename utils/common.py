#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm

"""
    General method
"""

import os
from utils.loggings import loggings

from sqlalchemy import CheckConstraint


def get_column_names(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(get_column_names(constraint))


# 连字符转驼峰
def str_format_convert(s):
    ss = ''
    for i in s.split('_'):
        if ss:
            ss += i.lower().capitalize()
        else:
            ss = i
    return ss


# 创建文件或文件夹
def new_file_or_dir(mode, url):
    try:
        if not os.path.exists(url):
            # new file
            if mode == 1:
                file = open(url, 'w')
                file.close()
            # new dir
            elif mode == 2:
                os.mkdir(url)
    except Exception as e:
        loggings.error(1, str(e))
