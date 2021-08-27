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

from utils.common import str_format_convert
from utils.loggings import loggings
from codegen.servicecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.servicecodegen.template.fileTemplate import FileTemplate
from utils.tablesMetadata import TableMetadata


class CodeGenerator(object):

    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata

    # resource layer generation
    def service_generator(self, service_path):
        try:
            table_dict = TableMetadata.get_tables_metadata(self.metadata)

            # Traverse each table to generate the corresponding service layer code
            for table in table_dict.keys():
                loggings.info(1, 'Generating service layer code for "{table_name}" table'.format(
                    table_name=table_dict[table]['table_name']))

                # The name of the table whose code needs to be generated
                table_name = str_format_convert(table_dict[table]['table_name'])
                table_name_initials_upper = table_name[0].upper() + table_name[1:]

                # Database query conditions
                filter_conditions = ""
                # Traverse each column to generate the filter conditions
                for columns in table_dict[table]['columns']:
                    columns_name = table_dict[table]['columns'][columns]['name']
                    filter_conditions += CodeBlockTemplate.single_filter_condition.format(colums_name=columns_name)

                # If there is a foreign key in the table, supplement the related template of the associated table
                # The following is an explanation of the variables required to generate the template file：
                # target_table_name: The name of the foreign key associated table (ps. Use CamelCase format)
                # target_table_name_initials_upper: Capitalize the name of the association table
                # foreign_import：If there is a foreign key in the table, add import statement
                # table_model: The string of using a comma to combine the name of this table and the associated table
                # join_table_statement: If there is a foreign key in the table, add join target table statement
                # result_name: The string of using underline to combine the name of this table and the associated table
                if foreign_key := table_dict[table].setdefault('foreign_keys', None):
                    target_table_name = str_format_convert(foreign_key['target_table'])
                    target_table_name_initials_upper = target_table_name[0].upper() + target_table_name[1:]
                    foreign_import = '\nfrom models.{0}Model import {1}'.format(target_table_name,
                                                                                target_table_name_initials_upper)
                    table_model = '{0}, {1}'.format(table_name_initials_upper, target_table_name_initials_upper)
                    join_table_statement = '.join("{0}")'.format(foreign_key['target_key'])
                    result_name = table_name + "_" + target_table_name + "_info"

                else:
                    foreign_import = ""
                    table_model = table_name_initials_upper
                    join_table_statement = ""
                    result_name = table_name + "_info"

                # Format the code block template
                imports = CodeBlockTemplate.service_import.format(table_name=table_name,
                                                                  table_name_initials_upper=table_name_initials_upper,
                                                                  foreign_import=foreign_import)

                # Format the file template
                template = FileTemplate.template.format(imports=imports,
                                                        table_name_initials_upper=table_name_initials_upper,
                                                        table_name=table_name,
                                                        foreign_import=foreign_import,
                                                        filter_conditions=filter_conditions,
                                                        table_model=table_model,
                                                        result_name=result_name,
                                                        join_table_statement=join_table_statement,
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
