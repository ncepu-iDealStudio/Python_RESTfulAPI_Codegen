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


# 连字符转驼峰
def str_format_convert(string):
    neo_string = ''
    for i in string.split('_'):
        if neo_string:
            neo_string += i.lower().capitalize()
        else:
            neo_string = i
    return neo_string