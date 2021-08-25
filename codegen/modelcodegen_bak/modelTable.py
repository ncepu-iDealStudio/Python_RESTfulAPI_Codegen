#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen.py
# author:https://github.com/agronholm/sqlacodegen
# datetime:2021/8/21 11:36
# software: PyCharm
"""
this is function description
"""
# import module your need
from sqlalchemy import Table

from codegen.modelcodegen_bak.model import Model


class ModelTable(Model):
    def __init__(self, table):
        super(ModelTable, self).__init__(table)
        self.name = self._convert_to_valid_identifier(table.name)

    def add_imports(self, collector):
        super(ModelTable, self).add_imports(collector)
        collector.add_import(Table)