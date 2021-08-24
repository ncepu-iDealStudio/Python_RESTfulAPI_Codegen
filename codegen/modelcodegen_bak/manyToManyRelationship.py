#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen.py
# author:https://github.com/agronholm/sqlacodegen
# datetime:2021/8/21 11:42
# software: PyCharm
"""
this is function description
"""
# import module your need
from sqlalchemy import ForeignKeyConstraint

from codegen.modelcodegen_bak.relationship import Relationship
from utils.common import get_constraint_sort_key, get_column_names


class ManyToManyRelationship(Relationship):
    def __init__(self, source_cls, target_cls, assocation_table):
        super(ManyToManyRelationship, self).__init__(source_cls, target_cls)

        prefix = (assocation_table.schema + '.') if assocation_table.schema else ''
        self.kwargs['secondary'] = repr(prefix + assocation_table.name)
        constraints = [c for c in assocation_table.constraints
                       if isinstance(c, ForeignKeyConstraint)]
        constraints.sort(key=get_constraint_sort_key)
        colname = get_column_names(constraints[1])[0]
        tablename = constraints[1].elements[0].column.table.name
        self.preferred_name = tablename if not colname.endswith('_id') else colname[:-3] + 's'

        # Handle self referential relationships
        if source_cls == target_cls:
            self.preferred_name = 'parents' if not colname.endswith('_id') else colname[:-3] + 's'
            pri_pairs = zip(get_column_names(constraints[0]), constraints[0].elements)
            sec_pairs = zip(get_column_names(constraints[1]), constraints[1].elements)
            pri_joins = ['{0}.{1} == {2}.c.{3}'.format(source_cls, elem.column.name,
                                                       assocation_table.name, col)
                         for col, elem in pri_pairs]
            sec_joins = ['{0}.{1} == {2}.c.{3}'.format(target_cls, elem.column.name,
                                                       assocation_table.name, col)
                         for col, elem in sec_pairs]
            self.kwargs['primaryjoin'] = (
                repr('and_({0})'.format(', '.join(pri_joins)))
                if len(pri_joins) > 1 else repr(pri_joins[0]))
            self.kwargs['secondaryjoin'] = (
                repr('and_({0})'.format(', '.join(sec_joins)))
                if len(sec_joins) > 1 else repr(sec_joins[0]))