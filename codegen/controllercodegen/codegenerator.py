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
from utils.common import str_format_convert
from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


class CodeGenerator(object):

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, controller_dir, rsa_table_column, primary_key_mode,
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
            business_key_init = ''
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
                        if table['business_key'].get('column') == column['name']:
                            text = CodeBlockTemplate.business_key_add.format(column=column['name'])
                            business_key_text = getattr(CodeBlockTemplate, table['business_key']['rule']).format(business_key=column['name'])
                            business_key_init += business_key_text
                        else:
                            # 本字段不是业务主键
                            text = CodeBlockTemplate.add_column_init.format(column=column['name'])
                else:
                    text = CodeBlockTemplate.rsa_add.format(column=column['name'])
                column_init += text
            add = FileTemplate.add_template.format(
                parent_model=parent_model,
                column_init=column_init,
                business_key_init=business_key_init,
                primary_key=primary_key
            )

            # combine get_filter_list
            get_filter_list = ''
            for column in table['columns'].values():
                if column['name'] == primary_key:
                    continue
                elif column['name'] == table['business_key'].get('column') and primary_key_mode == 'DoubleKey':
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
                primary_key=table['business_key']['column'] if primary_key_mode == 'DoubleKey' and table['business_key'].get('column') else primary_key,
                get_filter_list=get_filter_list,
                model_lower=table['table_name']
            )

            # combine delete
            if delete_way == 'logic':
                delete = FileTemplate.delete_template_logic.format(
                    primary_key=table['business_key']['column'] if primary_key_mode == 'DoubleKey' and table['business_key'].get('column') else primary_key
                )
            else:
                delete = FileTemplate.delete_template_physical.format(
                    primary_key=table['business_key']['column'] if primary_key_mode == 'DoubleKey' and table['business_key'].get('column') else primary_key
                )

            # combine update
            rsa_update = ''
            if rsa_table_column.get(table['table_name']):
                # several columns should be encrypted
                for sra_column in rsa_table_column[table['table_name']]:
                    text = CodeBlockTemplate.rsa_update.format(column=sra_column)
                    rsa_update += text
            update = FileTemplate.update_template.format(
                primary_key=table['business_key']['column'] if primary_key_mode == 'DoubleKey' and table['business_key'].get('column') else primary_key,
                rsa_update=rsa_update
            )

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
