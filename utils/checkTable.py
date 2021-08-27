#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkTable.py
# author:Itsuka
# datetime:2021/8/25 9:53
# software: PyCharm

"""
    this is function description
"""

import keyword

from sqlalchemy import create_engine, MetaData
from config.setting import Settings
from utils.loggings import loggings


class CheckTable(object):

    # 检查table主键
    @classmethod
    def check_primary_key(cls):
        """
        根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
        :return: 符合规范的表名列表，即有且仅有一个自增主键，没有符合规范的情况下返回None
        """
        url = Settings.MODEL_URL
        engine = create_engine(url)
        metadata = MetaData(engine)
        metadata.reflect(engine)
        tables = []
        # 根据代码生成模式获取表列表
        if Settings.CODEGEN_MODE == 'table':
            for i in Settings.MODEL_TABLES.replace(' ', '').split(','):
                tables.append(metadata.tables[i])
        elif Settings.CODEGEN_MODE == 'database':
            tables = metadata.tables.values()

        available_tables = []
        invalid_tables = []

        for table in tables:
            primary_flag = False  # 有无主键
            autoincrement_flag = False  # 是否自增
            repeat_flag = False  # 主键是否重复
            for column in table.c.values():
                if column.primary_key:
                    if not primary_flag:
                        primary_flag = True
                    else:
                        repeat_flag = True
                        break
                if column.primary_key and column.autoincrement:
                    autoincrement_flag = True
            if primary_flag and autoincrement_flag and not repeat_flag:
                available_tables.append(table.key)
            else:
                invalid_tables.append(table.key)

        if len(invalid_tables) > 0:
            loggings.warning(1,
                             "The following {0} tables do not meet the specifications and cannot be generated: {1}".format(
                                 len(invalid_tables), ",".join(invalid_tables)))
            return available_tables if available_tables else None

        loggings.info(1, "All table checks passed, a total of {0} tables ".format(len(tables)))
        return available_tables if available_tables else None

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword(cls, table_dict):
        """
        check the table name whether it is a keyword of python
        :return: True while no table name is a keyword, else return False
        """
        flag = True
        for table in table_dict.values():
            if keyword.iskeyword(table['table_name']):
                loggings.error(1, 'table "{}" is a keyword of python')
                flag = False
        return flag

    # check the foreign key
    # 检查表的外键约束
    @classmethod
    def check_foreign_key(cls, table_dict):
        """
        check whether the target table of the foreign key exists
        :return: True while the target table of the foreign key exists else False
        """
        flag = False
        for table in table_dict.values():
            if not table.get('foreign_keys'):
                continue
            # for foreign_key in table.get('foreign_key'):
            #     if not table_dict.get(foreign_key['target_table']):
            #         loggings.error(1, 'the foreign key of "{source_key}" in "{source_table}" does not exist')
            #         flag = False
            if not table_dict.get(table['foreign_keys']['target_table']):
                loggings.error(1, 'the target table "{target_table}" of foreign key "{source_table}.{source_key}" '
                                  'does not exist'.format(target_table=table['foreign_keys']['target_table'],
                                                          source_table=table['table_name'],
                                                          source_key=table['foreign_keys']['key']))
                flag = False
        return flag
