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
from decimal import Decimal

from utils.common import str_format_convert
from utils.loggings import loggings
from codegen.controllercodegen.template.filetemplate import FileTemplate
from codegen.controllercodegen.template.codeblocktemplate import CodeBlockTemplate

type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, controller_dir, delete_way='logic'):
        codes = {}
        # get table list
        table_name = self.metadata.tables.values()
        table_dict = {}

        # get columns attributes from each table
        for i in table_name:
            # get table
            table_dict[str(i)] = {}
            table_dict[str(i)]['columns'] = {}
            for j in i.c.values():
                # get column attributes
                table_dict[str(i)]['columns'][str(j.name)] = {}
                table_dict[str(i)]['columns'][str(j.name)]['name'] = j.name
                table_dict[str(i)]['columns'][str(j.name)]['primary_key'] = j.primary_key
                table_dict[str(i)]['columns'][str(j.name)]['autoincrement'] = j.autoincrement
                if j.type.python_type in type_map.keys():
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type]
                else:
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = 'str'

        # generate code and save in 'codes'
        for k, v in table_dict.items():
            hump_str = str_format_convert(k)
            model_name = hump_str
            class_name = hump_str[0].upper() + hump_str[1:] + 'Controller'
            parent_model = hump_str[0].upper() + hump_str[1:]

            # combine imports
            imports = CodeBlockTemplate.imports.format(model_name=model_name, parent_model=parent_model)
            basic = FileTemplate.basic_template.format(imports=imports, class_name=class_name,
                                                       parent_model=parent_model)

            # combine column_init
            column_init = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    continue
                else:
                    text = CodeBlockTemplate.add_column_init.format(column=column_k)
                    column_init += text
            add = FileTemplate.add_template.format(parent_model=parent_model, column_init=column_init)

            # combine get_filter_list
            get_filter_list = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    primary_key = column_k
                else:
                    if column_v['type'] in ['int', 'float']:
                        text = CodeBlockTemplate.get_filter_num.format(column=column_k)
                    else:
                        text = CodeBlockTemplate.get_filter_str.format(column=column_k)
                    get_filter_list += text
            get = FileTemplate.get_template.format(primary_key=primary_key, get_filter_list=get_filter_list, model_lower=k)

            # combine delete
            if delete_way == 'logic':
                delete = FileTemplate.delete_template_logic.format(primary_key=primary_key)
            else:
                delete = FileTemplate.delete_template_physical.format(primary_key=primary_key)

            # combine update
            update = FileTemplate.update_template.format(primary_key=primary_key)

            # save into 'codes'
            file_name = hump_str + 'Controller'
            codes[file_name] = basic + add + get + delete + update

        # generate files
        loggings.info(1, 'Generating __init__...')
        inti_file = os.path.join(controller_dir, '__init__.py')
        with open(inti_file, 'w', encoding='utf-8') as fw:
            fw.write(FileTemplate.init_template)
        loggings.info(1, '__init__ generated successfully')
        for k, v in codes.items():
            loggings.info(1, 'Generating {}...'.format(k))
            m_file = os.path.join(controller_dir, k + '.py')
            with open(m_file, 'w', encoding='utf-8') as fw:
                fw.write(v)
            loggings.info(1, '{} generated successfully'.format(k))
