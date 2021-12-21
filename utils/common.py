#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm

"""
    General method
"""


# 连字符转驼峰
def str_format_convert(string):
    neo_string = ''
    for i in string.split('_'):
        if neo_string:
            neo_string += i.lower().capitalize()
        else:
            neo_string = i
    return neo_string


# 转全小写
def str_to_all_small(string):
    neo_string = string.replace('_', '').lower()

    return neo_string


# 转小驼峰
def str_to_small_hump(string):
    neo_string = ''
    for i in string.split('_'):
        if neo_string:
            neo_string += i.capitalize()
        else:
            neo_string = i

    return neo_string


# 转大驼峰
def str_to_big_hump(string):
    neo_string = ''
    for i in string.split('_'):
        neo_string += i.capitalize()

    return neo_string
