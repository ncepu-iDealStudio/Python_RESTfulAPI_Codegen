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
from utils.common import str_format_convert, str_to_little_camel_case
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self, table_dict):
        self.table_dict = table_dict
        super().__init__()

    # resource layer generation
    def service_generator(self, service_path):
        try:
            # Traverse each table to generate the corresponding service layer code
            for table in self.table_dict.keys():
                loggings.info(1, 'Generating service layer code for "{table_name}" table'.format(
                    table_name=self.table_dict[table]['table_name']))

                # The name of the table whose code needs to be generated
                table_name = str_to_little_camel_case(self.table_dict[table]['table_name'])
                table_name_initials_upper = table_name[0].upper() + table_name[1:]

                # Format the code block template
                imports = CodeBlockTemplate.service_import.format(
                    table_name=table_name,
                    table_name_initials_upper=table_name_initials_upper,
                )

                # Format the file template
                template = FileTemplate.template.format(
                    imports=imports,
                    table_name_initials_upper=table_name_initials_upper,
                )

                # Write the template to the file
                with open(os.path.join(service_path, table_name + "Service.py"), 'w',
                          encoding='utf-8') as f:
                    f.write(template)

        except Exception as e:
            loggings.exception(1, e)
