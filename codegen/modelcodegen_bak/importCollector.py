#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen.py
# author:https://github.com/agronholm/sqlacodegen
# datetime:2021/8/21 11:44
# software: PyCharm
"""
this is function description
"""
# import module your need
from collections import OrderedDict
from importlib import import_module

import sqlalchemy


class ImportCollector(OrderedDict):
    def add_import(self, obj):
        """
            第一步： 判断传入对象的类型， 获取对象所在的模块
            第二步： 判断该模块是否是以 'sqlalchemy.dialects.' 开头的。
                    如果是则获取是一下是哪个数据库的。则记录一下是哪个'sqlalchemy.dialects.数据库'模块
                    如果不是，再看是这个模块是不是sqlalchemy当中的类型，来确定是否记录从salalchemy模块
                    否则 记录从对象所在模块
            第三步： 记录用键值对的方式记录从哪个没款导入哪个包

        """
        # 先看看obj这个对象的类型是否是 type（或者其子类） ，不是就设置为type（obj），是就设置为设置为obj
        type_ = type(obj) if not isinstance(obj, type) else obj
        # 获得当前操作对象在哪个模块
        pkgname = type_.__module__

        # The column types have already been adapted towards generic types if possible, so if this
        # is still a vendor specific type (e.g., MySQL INTEGER) be sure to use that rather than the
        # generic sqlalchemy type as it might have different constructor parameters.
        if pkgname.startswith('sqlalchemy.dialects.'):
            dialect_pkgname = '.'.join(pkgname.split('.')[0:3])
            dialect_pkg = import_module(dialect_pkgname)

            if type_.__name__ in dialect_pkg.__all__:
                pkgname = dialect_pkgname
        else:
            pkgname = 'sqlalchemy' if type_.__name__ in sqlalchemy.__all__ else type_.__module__
        self.add_literal_import(pkgname, type_.__name__)

    def add_literal_import(self, pkgname, name):
        names = self.setdefault(pkgname, set())
        names.add(name)
