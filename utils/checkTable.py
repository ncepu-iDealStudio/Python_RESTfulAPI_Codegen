#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkTable.py
# author:Itsuka
# datetime:2021/8/25 9:53
# software: PyCharm

"""
    检验表是否符合生成规则
"""

import keyword

from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


class CheckTable(object):

    # check the Primary key
    # 检查table主键
    @classmethod
    def check_primary_key(cls, table_dict, session_id, ip):
        """
        根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
        :return: 符合规范的表名列表，即有且仅有一个主键，没有符合规范的情况下返回None
        """

        available_tables = []
        invalid_tables = []

        for table in table_dict.values():

            if len(table['primary_key_columns']) == 0:
                # 表中没有主键
                invalid_tables.append(table['table_name'])
                loggings.warning(1, 'table {0} do not have a primary key'.format(table['table_name']), session_id, ip)
            elif len(table['primary_key_columns']) > 1:
                # 表中有复数个主键
                invalid_tables.append(table['table_name'])
                loggings.warning(1, 'table {0} has multiple primary keys'.format(table['table_name']))
            else:
                available_tables.append(table['table_name'])

        return available_tables, invalid_tables

    @classmethod
    def check_primary_key_update(cls, metadata, session_id, ip):
        """
                根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
                :return: 符合规范的表名列表，即有且仅有一个主键，没有符合规范的情况下返回None
                """

        available_tables = []
        invalid_tables = []

        # 获取所有表的信息
        all_tables = metadata.tables

        # 遍历所有表并判断是否有主键
        for table_name, table in all_tables.items():
            if table.primary_key:
                if len(table.primary_key) > 1:
                    invalid_tables.append(table_name)
                    loggings.warning(1, 'table {0} has multiple primary keys'.format(table_name))
                    # print(f"Table '{table_name}' has multiple primary keys: {table.primary_key}")
                else:
                    available_tables.append(table_name)
                    # print(f"Table '{table_name}' has a primary key.")
            else:
                # 表中没有主键
                invalid_tables.append(table_name)
                loggings.warning(1, 'table {0} do not have a primary key'.format(table_name), session_id, ip)
                # print(f"Table '{table_name}' does not have a primary key.")

        return available_tables, invalid_tables

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword_conflict_update(cls, metadata, session_id, ip):
        """
        check whether the table name or column name is a keyword of python
        :return: True while no table name is a keyword, else return False
        """

        available_tables = []
        invalid_tables = []

        # 获取所有表的信息
        all_tables = metadata.tables

        # 遍历所有表并判断是否有主键
        for table_name, table in all_tables.items():
            flag = True
            # 检查表名是否为python关键字
            if keyword.iskeyword(table_name.lower()):
                loggings.warning(1, 'table "{0}" is a keyword of python'.format(table_name), session_id,ip)
                flag = False

            # 检查字段名
            for column in table.columns:
                if keyword.iskeyword(column.name.lower()):
                    loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table_name,column),session_id,ip)
                    # print(f"Column name '{column.name}' in table '{table_name}' conflicts with a Python keyword.")
                    flag = False
            if flag:
                available_tables.append(table_name)
            else:
                invalid_tables.append(table_name)


        return available_tables, invalid_tables

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword_conflict(cls, table_dict, session_id, ip):
        """
        check whether the table name or column name is a keyword of python
        :return: True while no table name is a keyword, else return False
        """

        available_table = []
        invalid_table = []

        for table in table_dict.values():

            flag = True

            # 检查表名是否为python关键字
            if keyword.iskeyword(table['table_name']):
                loggings.warning(1, 'table "{0}" is a keyword of python'.format(table['table_name']), session_id, ip)
                flag = False

            for column in table['columns'].values():
                # 检查表字段是否为python关键字
                if keyword.iskeyword(column['name']):
                    loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table['table_name'],
                                                                                         column['name']), session_id,
                                     ip)
                    flag = False

            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])

        return available_table, invalid_table

    # 入口函数定义
    @classmethod
    def main(cls, metadata, session_id, ip, reflection_views, view=False):
        """
            建立数据库连接时对表进行检查，筛去没有唯一自增主键、表名/字段名与Python关键字有冲突的表
            :param metadata: 数据库元数据
            :param view: 是否为视图
        """
        if view:
            transformed_dict = TableMetadata.get_views_metadata(metadata, reflection_views)
            return transformed_dict
        else:
            transformed_dict = TableMetadata.get_tables_metadata(metadata, reflection_views)

        invalid_tables = {}

        # check table primary key
        available_table, invalid_table = cls.check_primary_key_update(metadata, session_id, ip)
        invalid_tables['primary_key'] = invalid_table
        for invalid in invalid_table:
            transformed_dict.pop(invalid)

        # check the keyword
        available_table, invalid_table = cls.check_keyword_conflict_update(metadata, session_id, ip)
        available_tables = available_table
        invalid_tables['keyword'] = invalid_table
        for invalid in invalid_table:
            transformed_dict.pop(invalid)

        if len(invalid_tables) > 0:
            loggings.warning(
                1,
                "A total of {0} tables check passed."
                "The following {1} tables do not meet the specifications and cannot be generated: {2}."
                .format(
                    len(available_tables),
                    len(invalid_tables['primary_key'] + invalid_tables['keyword']),
                    ",".join(invalid_tables['primary_key'] + invalid_tables['keyword'])
                ),
                session_id,
                ip
            )

            # # 反射数据库中的所有表
            # metadata.reflect()

            # 获取所有表的信息
            all_tables = metadata.tables
            tableMetadata=TableMetadata()

            # 遍历所有表
            for table_name, table in all_tables.items():
                transformed_dict[table_name]['columns']={}
                # 获取所有列的信息
                for column in table.c:
                    # 在这里继续你的逻辑处理

                    # 示例：输出列名和类型
                    transformed_dict[table_name]['columns'][str(column.name)] = {}
                    transformed_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

                    for type_ in tableMetadata.TYPE_MAPPING:
                        if str(metadata.bind.url).split('+')[0] != type_['database']:
                            continue
                        for python_type, sql_type_list in type_['data_map'].items():
                            if str(column.type).lower() in sql_type_list:
                                transformed_dict[table_name]['columns'][str(column.name)]['type'] = python_type
                                break
                    # print(f"Table: {table_name}, Column: {column.name}, Type: {column.type}")

                    # 存在复合主键
                    if len(transformed_dict[table_name]['primary_key_columns']) > 1:
                        transformed_dict[table_name]['business_key_column'] = {}
                    else:
                        # 如果主键不是自增的，则将业务主键设置为主键
                        if str(column.name) in transformed_dict[table_name]['primary_key_columns'] and not \
                                transformed_dict[table_name]['columns'][str(column.name)]['is_autoincrement']:
                            transformed_dict[table_name]['business_key_column']['column'] = str(column.name)

                    # 示例：判断是否是自动递增列
                    transformed_dict[table_name]['columns'][str(column.name)][
                        'is_autoincrement'] = True if column.autoincrement is True else False
                    # is_autoincrement = column.autoincrement if column.autoincrement is not None else False
                    # print(f"Is Autoincrement: {is_autoincrement}")

                    # 示例：判断是否可以为空
                    transformed_dict[table_name]['columns'][str(column.name)]['nullable'] = column.nullable
                    # nullable = column.nullable if column.nullable is not None else True
                    # print(f"Nullable: {nullable}")

                    # 示例：判断是否存在默认值
                    transformed_dict[table_name]['columns'][str(column.name)][
                        'is_exist_default'] = True if column.server_default is not None else False
                    # is_exist_default = column.server_default is not None
                    # print(f"Is Exist Default: {is_exist_default}")

            return transformed_dict, invalid_tables

        loggings.info(1, "All table checks passed, a total of {0} tables.".format(len(available_tables)), session_id,
                      ip)

        return transformed_dict, invalid_tables
