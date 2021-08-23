#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm
"""
this is function description
"""
# import module your need
# In SQLAlchemy 0.x, constraint.columns is sometimes a list, on 1.x onwards, always a
# ColumnCollection


from codegen.modelcodegen.codegen import CheckConstraint


def get_column_names(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(get_column_names(constraint))
