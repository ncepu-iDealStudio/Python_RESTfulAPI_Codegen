#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:tablesMetadata.py.py
# author:Nathan
# datetime:2021/8/26 14:56
# software: PyCharm

"""
    Get metadata of all tables
"""
import json


class TableMetadata(object):
    with open('config/default_table_config.json', 'r', encoding='utf-8') as f:
        DEFAULT_CONFIG = f.read()

    with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
        TYPE_MAPPING = json.load(f)

    @classmethod
    def get_tables_metadata(cls, metadata, table_config=DEFAULT_CONFIG):
        table_config = table_config if isinstance(table_config, list) else json.loads(table_config)

        # Get all tables object
        table_objs = metadata.tables.values()
        table_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        for table in table_objs:
            # get the table name
            table_name = str(table)
            table_dict[table_name] = {}
            table_dict[table_name]['table_name'] = table_name
            table_dict[table_name]['logical_delete_mark'] = ""
            table_dict[table_name]['columns'] = {}
            table_dict[table_name]['business_key'] = {}

            # Check if the business key exists and check record deletion method
            for config in table_config:
                if config['table'] == table_name and config['logicaldeletemark'] != '':
                    table_dict[table_name]['logical_delete_mark'] = config['logicaldeletemark']

                if config['table'] == table_name and config['businesskeyname'] != '':
                    table_dict[table_name]['business_key']['column'] = config['businesskeyname']
                    table_dict[table_name]['business_key']['rule'] = config['businesskeyrule']

            # 需要RSA加密的字段
            table_dict[table_name]['rsa_columns'] = []
            for rsa_table in table_config:
                if rsa_table['table'] == table_name:
                    for rsa_colume in rsa_table['field']:
                        if rsa_colume['field_encrypt']:
                            table_dict[table_name]['rsa_columns'].append(rsa_colume['field_name'])

            # 初始化为空列表
            table_dict[table_name]['primaryKey'] = []

            # Traverse each columns to get corresponding attributes
            for column in table.columns.values():
                table_dict[table_name]['columns'][str(column.name)] = {}
                table_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

                for type_ in cls.TYPE_MAPPING:
                    if str(metadata.bind.url).split('+')[0] != type_['database']:
                        continue
                    for python_type, sql_type_list in type_['data_map'].items():
                        if str(column.type).lower() in sql_type_list:
                            table_dict[table_name]['columns'][str(column.name)]['type'] = python_type
                            break
                table_dict[table_name]['columns'][str(column.name)].setdefault('type', 'str')

                if column.primary_key:
                    table_dict[table_name]['primaryKey'].append(str(column.name))

                # 是否自动递增
                table_dict[table_name]['columns'][str(column.name)][
                    'is_autoincrement'] = True if column.autoincrement is True else False

                # 如果主键不是自增的，则将业务主键设置为主键
                if str(column.name) in table_dict[table_name]['primaryKey'] and not \
                        table_dict[table_name]['columns'][str(column.name)]['is_autoincrement']:
                    table_dict[table_name]['business_key']['column'] = str(column.name)

                # 是否可以为空
                table_dict[table_name]['columns'][str(column.name)]['nullable'] = column.nullable

                # 是否存在默认值
                table_dict[table_name]['columns'][str(column.name)][
                    'is_exist_default'] = True if column.server_default is not None else False

        return table_dict
