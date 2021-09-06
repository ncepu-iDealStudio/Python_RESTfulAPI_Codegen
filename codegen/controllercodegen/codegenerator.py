#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegenerator.py
# author:Itsuka
# datetime:2021/8/24 10:04
# software: PyCharm

"""
    generate controller layer code
    This generator is a very simple boilerplate for generate controller code with Flask, flask-restful,
    marshmallow, SQLAlchemy and jwt.
    It comes with basic project structure and configuration, including blueprints, application factory
    and basics unit tests.
"""

import os.path

from codegen.controllercodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.controllercodegen.template.filetemplate import FileTemplate
from config.natural_key_template import natural_key_template_dict
from utils.common import str_format_convert
from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


class CodeGenerator(object):

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, controller_dir, rsa_table_column, business_key_list, primary_key_mode,
                           delete_way='logic'):
        codes = {}
        # get table metadata
        table_dict = TableMetadata.get_tables_metadata(self.metadata)

        # generate code and save in 'codes'
        for table in table_dict.values():
            hump_str = str_format_convert(table['table_name'])
            model_name = hump_str + 'Model'
            class_name = hump_str[0].upper() + hump_str[1:] + 'Controller'
            parent_model = hump_str[0].upper() + hump_str[1:]
            primary_key = table['primaryKey']

            # combine imports
            imports = CodeBlockTemplate.imports.format(model_name=model_name, parent_model=parent_model)
            basic = FileTemplate.basic_template.format(imports=imports, class_name=class_name,
                                                       parent_model=parent_model)

            # combine column_init
            column_init = ''
            for column in table['columns'].values():
                if column['name'] == primary_key:
                    continue
                # the column do not encrypt
                elif not rsa_table_column.get(table['table_name']) or column['name'] not in rsa_table_column[table['table_name']]:
                    if primary_key_mode == 'AutoID':
                        # 仅自增主键模式
                        text = CodeBlockTemplate.add_column_init.format(column=column['name'])
                    else:
                        # 业务主键模式
                        flag = True
                        for natural_key_table_column in business_key_list:
                            if table['table_name'] == natural_key_table_column['table'] and column['name'] == natural_key_table_column['column']:
                                natural_key_template = natural_key_table_column.get('template') if natural_key_table_column.get('template') else 'default'
                                if natural_key_template:
                                    text = natural_key_template_dict[natural_key_table_column['template']].format(natural_key=natural_key_table_column['column'])
                                flag = False
                                break
                        if flag:
                            text = CodeBlockTemplate.add_column_init.format(column=column['name'])
                else:
                    text = CodeBlockTemplate.rsa_add.format(column=column['name'])
                column_init += text
            add = FileTemplate.add_template.format(parent_model=parent_model, column_init=column_init)

            # combine get_filter_list
            get_filter_list = ''
            for column in table['columns'].values():
                if column['name'] == primary_key:
                    continue
                else:
                    if column['type'] in ['int', 'float']:
                        # column type is a number
                        if not rsa_table_column.get(table['table_name']) or column['name'] not in rsa_table_column.get(table['table_name']):
                            # column do not encrypt
                            text = CodeBlockTemplate.get_filter_num.format(column=column['name'])
                        else:
                            text = CodeBlockTemplate.rsa_get_filter_num.format(column=column['name'])
                    else:
                        # column type is a string
                        if not rsa_table_column.get(table['table_name']) or column['name'] not in rsa_table_column.get(table['table_name']):
                            # column do not encrypt
                            text = CodeBlockTemplate.get_filter_str.format(column=column['name'])
                        else:
                            text = CodeBlockTemplate.rsa_get_filter_str.format(column=column['name'])
                    get_filter_list += text
            get = FileTemplate.get_template.format(
                primary_key=primary_key,
                get_filter_list=get_filter_list,
                model_lower=table['table_name']
            )

            # combine delete
            if delete_way == 'logic':
                delete = FileTemplate.delete_template_logic.format(primary_key=primary_key)
            else:
                delete = FileTemplate.delete_template_physical.format(primary_key=primary_key)

            # combine update
            rsa_update = ''
            if rsa_table_column.get(table['table_name']):
                # several columns should be encrypted
                for sra_column in rsa_table_column[table['table_name']]:
                    text = CodeBlockTemplate.rsa_update.format(column=sra_column)
                    rsa_update += text
            update = FileTemplate.update_template.format(primary_key=primary_key, rsa_update=rsa_update)

            # save into 'codes'
            file_name = hump_str + 'Controller'
            codes[file_name] = basic + add + get + delete + update

        # generate files
        loggings.info(1, 'Generating __init__...')
        inti_file = os.path.join(controller_dir, '__init__.py')
        with open(inti_file, 'w', encoding='utf-8') as fw:
            fw.write(FileTemplate.init_template)
        loggings.info(1, '__init__ generated successfully')
        for file_name, code in codes.items():
            loggings.info(1, 'Generating {}...'.format(file_name))
            m_file = os.path.join(controller_dir, file_name + '.py')
            with open(m_file, 'w', encoding='utf-8') as fw:
                fw.write(code)
            loggings.info(1, '{} generated successfully'.format(file_name))
