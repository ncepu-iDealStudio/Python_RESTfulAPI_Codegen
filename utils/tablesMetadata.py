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

from config.setting import Settings


class TableMetadata(object):
    with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
        type_mapping = json.load(f)

    database_type = Settings.DATABASE_TYPE

    @classmethod
    def get_tables_metadata(cls, metadata):
        # Get all tables object
        table_objs = metadata.tables.values()
        table_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        for table in table_objs:
            # get the table name
            table_name = str(table)
            table_dict[table_name] = {}
            table_dict[table_name]['columns'] = {}
            table_dict[table_name]['table_name'] = table_name
            table_dict[table_name]['foreign_keys'] = []

            # Traverse each columns to get corresponding attributes
            for column in table.columns.values():
                table_dict[table_name]['columns'][str(column.name)] = {}
                table_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

                for type_ in cls.type_mapping:
                    if cls.database_type != type_['database']:
                        continue
                    for python_type, sql_type_list in type_['data_map'].items():
                        if str(column.type).lower() in sql_type_list:
                            table_dict[table_name]['columns'][str(column.name)]['type'] = python_type
                            break
                table_dict[table_name]['columns'][str(column.name)].setdefault('type', 'str')

                if column.primary_key:
                    table_dict[table_name]['primaryKey'] = str(column.name)

                if column.foreign_keys:
                    # Traverse each foreign_key to get corresponding attributes
                    for foreign_key in column.foreign_keys:
                        table_dict[table_name]['foreign_keys'].append({
                            'key': str(column.name),
                            'target_table': str(foreign_key.column).split('.')[0],
                            'target_key': str(foreign_key.column).split('.')[1]
                        })
        return table_dict
