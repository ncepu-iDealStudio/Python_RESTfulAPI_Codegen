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


# 文件写入
def file_write(path, content):
    new_file_or_dir(1, path)
    with open(path, 'w', encoding='utf8') as f:
        f.write(content)
