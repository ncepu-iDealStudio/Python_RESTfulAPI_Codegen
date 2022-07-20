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

from codegen.servicecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.servicecodegen.template.fileTemplate import FileTemplate
from utils.common import str_to_little_camel_case, str_to_all_small
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self, table_dict, session_id, ip):
        self.table_dict = table_dict
        self.session_id = session_id
        self.ip = ip
        super().__init__()

    # resource layer generation
    def service_generator(self, service_path):
        try:
            # Traverse each table to generate the corresponding service layer code
            for table in self.table_dict.keys():
                loggings.info(1, 'Generating service layer code for "{table_name}" table'.format(
                    table_name=self.table_dict[table]['table_name']), self.session_id, self.ip)

                table_name = str_to_little_camel_case(self.table_dict[table]['table_name'])
                table_name_initials_upper = table_name[0].upper() + table_name[1:]
                # 该表为基本表
                if not self.table_dict[table]['is_view']:
                    imports = CodeBlockTemplate.service_table_import.format(
                        table_name=table_name,
                        table_name_initials_upper=table_name_initials_upper,
                    )

                    # Format the file template
                    template = FileTemplate.table_template.format(
                        imports=imports,
                        table_name_initials_upper=table_name_initials_upper,
                    )

                # 该表为视图
                else:
                    imports = CodeBlockTemplate.service_view_import.format(
                        view_name=str_to_little_camel_case(self.table_dict[table]['table_name']),
                        original_view_name=self.table_dict[table]['table_name'],
                    )
                    filter_condition = ""
                    for column in self.table_dict[table]['filter_field']:
                        if column['field_type'] == "str":
                            filter_condition += CodeBlockTemplate.filter_conditions_for_str.format(
                                column=column['field_name'],
                                original_view_name=self.table_dict[table]['table_name']
                            )
                        else:
                            filter_condition += CodeBlockTemplate.filter_conditions.format(
                                column=column['field_name'],
                                original_view_name=self.table_dict[table]['table_name']
                            )

                    # Format the file template
                    template = FileTemplate.view_template.format(
                        imports=imports,
                        table_name_initials_upper=table_name_initials_upper,
                        filter_conditions=filter_condition,
                        original_view_name=self.table_dict[table]['table_name'],
                        table_name_lower_case=str_to_all_small(self.table_dict[table]['table_name'], )
                    )

                # Write the template to the file
                with open(os.path.join(service_path, table_name + "Service.py"), 'w',
                          encoding='utf-8') as f:
                    f.write(template)
        except Exception as e:
            loggings.exception(1, e, self.session_id, self.ip)
