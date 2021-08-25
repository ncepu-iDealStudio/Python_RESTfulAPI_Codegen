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

from utils.response_code import RET
from utils.common import str_format_convert, new_file_or_dir
from .template import fileFormat, strFormat

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
                    else:
                        return {'code': RET.DBERR, 'message': '{0}表内存在多个主键'.format(str(i)),
                                'error': '{0}表内存在多个主键'.format(str(i))}
                if j.type.python_type in type_map.keys():
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type]
                else:
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = 'str'

        # Init generation
        for table in table_dict.keys():
            # Init generation
            init_list = self.init_codegen(table_dict[table]).replace('\"', '\'')
            # print(init_list)
            # Urls generation
            urls_list = self.urls_codegen(table_dict[table]).replace('\"', '\'')
            # print(urls_list)
            # Resource generation
            resource_list = self.resource_codegen(table_dict[table]).replace('\"', '\'')
            # print(resource_list)
            # OtherResource generation
            otherResource_list = self.other_resource_codegen(table_dict[table]).replace('\"', '\'')
            # print(otherResource_list)

            resource_dir = os.path.join(target_dir, '{0}Resource'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(2, resource_dir)

            init_file = os.path.join(resource_dir, '__init__.py')
            new_file_or_dir(1, init_file)

            urls_file = os.path.join(resource_dir, 'urls.py')
            new_file_or_dir(1, urls_file)

            resource_file = os.path.join(resource_dir, '{0}Resource.py'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(1, resource_file)

            other_resource_file = os.path.join(resource_dir, '{0}OtherResource.py'.format(str_format_convert(
                table_dict[table].get('tableName')
            )))
            new_file_or_dir(1, other_resource_file)

            # File write
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
        blueprint_str = strFormat.blueprint_format.format(blueprint_name.lower(), blueprint_name)
        return fileFormat.template_init.format(blueprint=blueprint_str)

    #  urls generation
    def urls_codegen(self, table):
        # Remove underline
        api_name = str_format_convert(table.get('tableName'))
        # Template  generation
        import_str = strFormat.urls_imports_format.format(api_name.lower(), api_name, api_name.capitalize())

        api_str = strFormat.api_format.format(api_name)

        primary_key_str = strFormat.primary_key_format.format(str_format_convert(table.get('primaryKey')))
        resource_str = strFormat.resource_format.format(api_name.capitalize(), primary_key_str, api_name)

        other_resource_str = strFormat.other_resource_format.format(api_name.capitalize(), api_name)

        return fileFormat.template_urls.format(
            imports=import_str, api=api_str, resource=resource_str, otherResource=other_resource_str)

    # resource generation 
    def resource_codegen(self, table):
        # Remove underline
        api_name = str_format_convert(table.get('tableName'))

        # Template  generation
        imports_str = strFormat.resource_imports_format.format(api_name)

        className_str = api_name.capitalize()

        id_str = table.get('primaryKey')

        # Get field list (except primary key)
        argument_str = ''
        for j in table.get('columns').values():
            if j.get('name') != table.get('primaryKey'):
                argument_str += strFormat.arguement_format.format(j.get('name'), j.get('type'))

        idCheck_str = strFormat.id_check_format.format(id_str)

        getControllerInvoke_str = strFormat.get_controller_invoke_format.format(className_str)

        deleteControllerInvoke_str = strFormat.delete_controller_invoke_format.format(className_str)

        putControllerInvoke_str = strFormat.put_controller_invoke_format.format(className_str)

        return fileFormat.template_resource.format('{}', imports=imports_str, className=className_str, id=id_str,
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
        imports_str = strFormat.resource_imports_format.format(api_name)

        className_str = api_name.capitalize()

        id_str = table.get('primaryKey')

        # Get field list (except primary key)
        argument_str = ''
        for j in table.get('columns').values():
            if j.get('name') != table.get('primaryKey'):
                argument_str += strFormat.arguement_format.format(j.get('name'), j.get('type'))

        getControllerInvoke_str = strFormat.get_controller_invoke_format.format(table.get('tableName'))

        postControllerInvoke_str = strFormat.post_controller_invoke_format.format(table.get('tableName'))

        return fileFormat.template_other_resource.format(imports=imports_str, className=className_str, id=id_str,
                                                         argument=argument_str,
                                                         getControllerInvoke=getControllerInvoke_str,
                                                         postControllerInvoke=postControllerInvoke_str
                                                         )