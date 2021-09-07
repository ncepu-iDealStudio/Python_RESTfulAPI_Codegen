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
from utils.tablesMetadata import TableMetadata


class CheckTable(object):

    # check the Primary key
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

        return available_tables, invalid_tables

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword_conflict(cls, table_dict):
        """
        check whether the table name or column name is a keyword of python
        :return: True while no table name is a keyword, else return False
        """
        available_table = []
        invalid_table = []
        for table in table_dict.values():
            flag = True
            if keyword.iskeyword(table['table_name']):
                loggings.warning(1, 'table "{0}" is a keyword of python'.format(table['table_name']))
                flag = False
            for column in table['columns'].values():
                if keyword.iskeyword(column['name']):
                    loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table['table_name'],
                                                                                         column['name']))
                    flag = False
            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])
        return available_table, invalid_table

    # check the foreign key
    # 检查表的外键约束
    @classmethod
    def check_foreign_key(cls, table_dict):
        """
        check whether the target table of the foreign key exists
        :return: True while the target table of the foreign key exists else False
        """
        available_table = []
        invalid_table = []
        for table in table_dict.values():
            flag = True
            if not table.get('foreign_keys'):
                available_table.append(table['table_name'])
                continue
            for foreign_key in table.get('foreign_keys'):
                if not table_dict.get(foreign_key['target_table']):
                    loggings.waring(1, 'the target table or column "{target_table}.{target_key}" of "{source_table}.'
                                       '{source_key}" does not exist'.format(target_table=foreign_key['target_table'],
                                                                             target_key=foreign_key['target_key'],
                                                                             source_table=table['table_name'],
                                                                             source_key=foreign_key['key']))
                    flag = False
            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])
        return available_table, invalid_table

    # 检查业务主键是否存在
    @classmethod
    def check_natural_key(cls, table_dict):
        """
        检查业务主键是否存在以及是否与自增主键重复
        :return: 符合生成规则的表列表available_table和不符合生成规则的表列表invalid_table
        """
        available_table = [x['table_name'] for x in table_dict.values()]
        invalid_table = []
        business_key_list = Settings.BUSINESS_KEY_LIST
        for natural_key in business_key_list:
            flag = True
            # 检查表是否存在
            if natural_key['table'] not in available_table:
                flag = False
                loggings.warning(1, 'the target table {table} of natural key {table}.{column} '
                                    'does not exist'.format(table=natural_key['table'],
                                                            column=natural_key['column']))
            if not flag:
                continue

            # 检查字段是否存在
            if natural_key['column'] not in table_dict[natural_key['table']]['columns'].keys():
                flag = False
                loggings.warning(1, 'the column of natural key {table}.{column} does not exist '
                                    'in table {table}'.format(table=natural_key['table'],
                                                              column=natural_key['column']))
                invalid_table.append(available_table.pop(available_table.index(natural_key['table'])))
            if not flag:
                continue

            # 检查业务主键是否与自增主键重复
            if natural_key['column'] == table_dict[natural_key['table']]['primaryKey']:
                loggings.warning(1, 'the natural key {table}.{column} is an Auto increment '
                                    'primary key '.format(table=natural_key['table'],
                                                          column=natural_key['column']))
                invalid_table.append(available_table.pop(available_table.index(natural_key['table'])))

        return available_table, invalid_table

    # 入口函数定义
    @classmethod
    def main(cls):

        url = Settings.MODEL_URL
        engine = create_engine(url)
        metadata = MetaData(engine)
        metadata.reflect(engine)

        # check table primary key
        available_tables, invalid_tables = cls.check_primary_key()

        # check the foreign key
        metadata = MetaData(engine)
        metadata.reflect(engine, only=available_tables)
        table_dict = TableMetadata.get_tables_metadata(metadata)
        available_table, invalid_table = cls.check_foreign_key(table_dict)
        available_tables = available_table
        invalid_tables += invalid_table

        # check the keyword
        metadata = MetaData(engine)
        metadata.reflect(engine, only=available_tables)
        table_dict = TableMetadata.get_tables_metadata(metadata)
        available_table, invalid_table = cls.check_keyword_conflict(table_dict)
        available_tables = available_table
        invalid_tables += invalid_table

        # check the natural key
        metadata = MetaData(engine)
        metadata.reflect(engine, only=available_tables)
        table_dict = TableMetadata.get_tables_metadata(metadata)
        available_table, invalid_table = cls.check_natural_key(table_dict)
        available_tables = available_table
        invalid_tables += invalid_table

        if len(invalid_tables) > 0:
            loggings.warning(1, "The following {0} tables do not meet the specifications and cannot "
                                "be generated: {1}".format(len(invalid_tables), ",".join(invalid_tables)))
            return available_tables if available_tables else None

        loggings.info(1, "All table checks passed, a total of {0} "
                         "tables ".format(len(available_tables + invalid_tables)))
        return available_tables if available_tables else None
