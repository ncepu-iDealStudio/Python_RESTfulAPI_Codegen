#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/25 11:12
# software: PyCharm

"""
    初始化model层所需参数
"""

cmd = "flask-sqlacodegen {url}{schema}{tables}{noviews}{noindexes}" \
      " {noconstraints}{nojoined}{noinflect}{noclasses}{notables}{outfile}{nobackrefs}" \
      " {nocomments}{ignore_cols} --flask"
