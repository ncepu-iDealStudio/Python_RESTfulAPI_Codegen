#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegenerator.py
# author:Nathan
# datetime:2021/8/26 11:41
# software: PyCharm

"""
    this is function description
"""

import os
from decimal import Decimal

from utils.common import str_format_convert
from utils.loggings import loggings
from .codeblocktemplate import CodeBlockTemplate
from .fileTemplate import FileTemplate

type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):

    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata

    # resource layer generation
    def service_generator(self, service_path):
        try:
            # get the table list
            table_names = self.metadata.tables.values()

            table_dict = {}
            # get the field list, primary key and table name of each table
            for i in table_names:
                # get the table
                table_dict[str(i)] = {}
                table_dict[str(i)]['columns'] = {}
                table_dict[str(i)]['tableName'] = str(i)
                for j in i.c.values():
                    table_dict[str(i)]['columns'][str(j.name)] = {}
                    table_dict[str(i)]['columns'][str(j.name)]['name'] = str(j.name)
                    if j.primary_key:
                        if not table_dict[str(i)].get('primaryKey'):
                            table_dict[str(i)]['primaryKey'] = str(j.name)
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type] if type_map.get(
                        j.type.python_type) else 'str'

            # Traverse each table to generate the corresponding service layer code
            for table in table_dict.keys():
                loggings.info(1, 'Generating service layer code for "{table_name}" table'.format(
                    table_name=table_dict[table]['tableName']))
                table_name = str_format_convert(table_dict[table]['tableName'])
                class_name = table_name[0].upper() + table_name[1:] + "Service"
                super_class_name = table_name[0].upper() + table_name[1:] + "Controller"
                function_name = "query_" + table_name
                result_name = table_name + "_info"
                imports = CodeBlockTemplate.service_import.format(table_name=table_name,
                                                                  table_name_upper=super_class_name)
                filter_conditions = ""

                Fields_list = []
                # Traverse each column to generate the filter_condition and the Fields
                for columns in table_dict[table]['columns']:
                    columns_name = table_dict[table]['columns'][columns]['name']
                    filter_conditions += CodeBlockTemplate.single_filter_condition.format(colums_name=columns_name)
                    Fields_list.append("cls.{columns_name}".format(columns_name=columns_name))

                Fields = ', '.join(Fields_list)

                # format file template
                template = FileTemplate.template.format(imports=imports,
                                                        class_name=class_name,
                                                        super_class_name=super_class_name,
                                                        function_name=function_name,
                                                        filter_conditions=filter_conditions,
                                                        result_name=result_name,
                                                        Fields=Fields,
                                                        exception_return=CodeBlockTemplate.exception_return,
                                                        notdata_return=CodeBlockTemplate.notdata_return,
                                                        success_return=CodeBlockTemplate.success_return
                                                        )

                # Write the template to the file
                with open(os.path.join(service_path, table_name + "Service"), 'w',
                          encoding='utf-8') as f:
                    f.write(template)

        except Exception as e:
            loggings.error(1, str(e))
