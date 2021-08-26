#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:tablesMetadata.py.py
# author:Nathan
# datetime:2021/8/26 14:56
# software: PyCharm

"""
    Get metadata
"""

from decimal import Decimal


class TableMetadata(object):
    type_map = {
        int: 'int',
        float: 'float',
        Decimal: 'float'
    }

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

            # Traverse each columns to get corresponding attributes
            for column in table.columns.values():
                table_dict[table_name]['columns'][str(column.name)] = {}
                table_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

                # Possibly incomplete consideration of field types
                table_dict[table_name]['columns'][str(column.name)]['type'] = TableMetadata.type_map[
                    column.type.python_type] if TableMetadata.type_map.get(column.type.python_type) else 'str'

                if column.primary_key:
                    table_dict[table_name]['primaryKey'] = str(column.name)

                if column.foreign_keys:
                    table_dict[table_name]['foreign_keys'] = {}
                    # Traverse each foreign_key to get corresponding attributes
                    for foreign_key in column.foreign_keys:
                        table_dict[table_name]['foreign_keys']['key'] = str(column.name)
                        table_dict[table_name]['foreign_keys']['target_table'] = str(foreign_key.column).split('.')[0]
                        table_dict[table_name]['foreign_keys']['target_key'] = str(foreign_key.column).split('.')[1]

        return table_dict
