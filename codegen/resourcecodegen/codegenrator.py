#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen.py
# author:PigKnight
# datetime:2021/8/23 8:45
# software: PyCharm

"""
  generate resource lay code.
  This generator is a very simple boilerplate for generate a REST api using Flask, flask-restful,  marshmallow, SQLAlchemy and jwt.
  It comes with basic project structure and configuration, including blueprints, application factory and basics unit tests.
"""

import os
from decimal import Decimal

from utils.loggings import loggings
from utils.response_code import RET
from config.setting import Settings
from utils.common import str_format_convert, new_file_or_dir
from .template import FileTemplate, CodeBlockTemplate

type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    # Resource layer generation
    def resource_generator(self, target_dir):
        # Get the table list
        table_names = self.metadata.tables.values()
        table_dict = {}
        # Get the field list, primary key and table name of each table
        for i in table_names:
            # Get the table
            table_dict[str(i)] = {}
            table_dict[str(i)]['columns'] = {}
            table_dict[str(i)]['tableName'] = str(i)
            for j in i.c.values():
                table_dict[str(i)]['columns'][str(j.name)] = {}
                table_dict[str(i)]['columns'][str(j.name)]['name'] = str(j.name)
                if j.primary_key:
                    if not table_dict[str(i)].get('primaryKey'):
                        table_dict[str(i)]['primaryKey'] = str(j.name)
                table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type] if type_map.get(j.type.python_type) else 'str'
        # File generation
        for table in table_dict.keys():
            resource_dir = os.path.join(target_dir, '{0}Resource'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(2, resource_dir)

            # Init generation
            init_file = os.path.join(resource_dir, '__init__.py')
            new_file_or_dir(1, init_file)
            init_list = self.init_codegen(table_dict[table]).replace('\"', '\'')
            # print(init_list)

            # Urls generation
            urls_file = os.path.join(resource_dir, 'urls.py')
            new_file_or_dir(1, urls_file)
            urls_list = self.urls_codegen(table_dict[table]).replace('\"', '\'')
            # print(urls_list)

            # Resource generation
            resource_file = os.path.join(resource_dir, '{0}Resource.py'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(1, resource_file)
            resource_list = self.resource_codegen(table_dict[table]).replace('\"', '\'')
            # print(resource_list)

            # OtherResource generation
            other_resource_file = os.path.join(resource_dir, '{0}OtherResource.py'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(1, other_resource_file)
            otherResource_list = self.other_resource_codegen(table_dict[table]).replace('\"', '\'')
            # print(otherResource_list)

            # File write
            loggings.info(1, 'Generating {0}Resource'.format(table_dict[table].get('tableName')))
            with open(init_file, 'w', encoding='utf8') as f:
                f.write(init_list)
            with open(urls_file, 'w', encoding='utf8') as f:
                f.write(urls_list)
            with open(resource_file, 'w', encoding='utf8') as f:
                f.write(resource_list)
            with open(other_resource_file, 'w', encoding='utf8') as f:
                f.write(otherResource_list)

    # init generation
    def init_codegen(self, table):
        # Remove underline
        blueprint_name = str_format_convert(table.get('tableName'))
        # Template generation
        blueprint_str = CodeBlockTemplate.init_blueprint.format(blueprint_name.lower(), blueprint_name)
        return FileTemplate.init.format(blueprint=blueprint_str)

    #  urls generation
    def urls_codegen(self, table):
        # Remove underline
        api_name = str_format_convert(table.get('tableName'))
        # Template  generation
        import_str = CodeBlockTemplate.urls_imports.format(api_name.lower(), Settings.API_VERSION, api_name, api_name.capitalize())

        api_str = CodeBlockTemplate.urls_api.format(api_name)

        primary_key_str = CodeBlockTemplate.primary_key.format(
            api_name, str_format_convert(table.get('primaryKey')))
        resource_str = CodeBlockTemplate.urls_resource.format(api_name.capitalize(), primary_key_str, api_name)

        other_resource_str = CodeBlockTemplate.urls_other_resource.format(api_name.capitalize(), api_name, api_name)

        return FileTemplate.urls.format(
            imports=import_str, api=api_str, resource=resource_str, otherResource=other_resource_str)

    # resource generation 
    def resource_codegen(self, table):
        # Remove underline
        api_name = str_format_convert(table.get('tableName'))

        # Template  generation
        imports_str = CodeBlockTemplate.resource_imports.format(api_name)

        className_str = api_name.capitalize()

        id_str = table.get('primaryKey')

        # Get field list (except primary key)
        argument_str = ''
        for j in table.get('columns').values():
            if j.get('name') != table.get('primaryKey'):
                argument_str += CodeBlockTemplate.parameter.format(j.get('name'), j.get('type'))

        idCheck_str = CodeBlockTemplate.resource_id_check.format(id_str)

        getControllerInvoke_str = CodeBlockTemplate.get_controller_invoke.format(className_str)

        deleteControllerInvoke_str = CodeBlockTemplate.resource_delete_controller_invoke.format(className_str)

        putControllerInvoke_str = CodeBlockTemplate.resource_put_controller_invoke.format(className_str)

        return FileTemplate.resource.format('{}', imports=imports_str, className=className_str, id=id_str,
                                            idCheck=idCheck_str, argument=argument_str,
                                            getControllerInvoke=getControllerInvoke_str,
                                            deleteControllerInvoke=deleteControllerInvoke_str,
                                            putControllerInvoke=putControllerInvoke_str
                                            )

    # otherResource generation 
    def other_resource_codegen(self, table):
        # Remove underline
        api_name = str_format_convert(table.get('tableName'))

        # Template generation
        imports_str = CodeBlockTemplate.resource_imports.format(api_name)

        className_str = api_name.capitalize()

        id_str = table.get('primaryKey')

        # Get field list (except primary key)
        argument_str = ''
        for j in table.get('columns').values():
            if j.get('name') != table.get('primaryKey'):
                argument_str += CodeBlockTemplate.parameter.format(j.get('name'), j.get('type'))

        getControllerInvoke_str = CodeBlockTemplate.get_controller_invoke.format(table.get('tableName'))

        postControllerInvoke_str = CodeBlockTemplate.other_resource_post_controller_invoke.format(table.get('tableName'))

        return FileTemplate.other_resource.format(imports=imports_str, className=className_str, id=id_str,
                                                  argument=argument_str,
                                                  getControllerInvoke=getControllerInvoke_str,
                                                  postControllerInvoke=postControllerInvoke_str
                                                  )
