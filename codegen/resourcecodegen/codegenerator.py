#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqlacodegen.py
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
from config.setting import Settings
from utils.common import str_format_convert, new_file_or_dir, file_write
from . import codegenLayer, tables, metadata
from codegen.resourcecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.resourcecodegen.template.filetemplate import FileTemplate

type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    # resource layer generation
    def resource_generator(self, api_dir, app_dir):
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
            # app generation
            loggings.info(1, 'Start generating API layer, please wait...')
            self.app_codegen(app_dir, table_dict)
            loggings.info(1, 'Generating API layer complete')
            # file generation
            for table in table_dict.keys():
                resource_dir = os.path.join(api_dir, '{0}Resource'.format(str_format_convert(
                    table_dict[table].get('tableName')
                )))
                new_file_or_dir(2, resource_dir)

                # init generation
                init_file = os.path.join(resource_dir, '__init__.py')
                init_list = self.init_codegen(table_dict[table]).replace('\"', '\'')

                # urls generation
                urls_file = os.path.join(resource_dir, 'urls.py')
                urls_list = self.urls_codegen(table_dict[table]).replace('\"', '\'')

                # resource generation
                resource_file = os.path.join(resource_dir, '{0}Resource.py'.format(str_format_convert(
                    table_dict[table].get('tableName')
                )))
                resource_list = self.resource_codegen(table_dict[table]).replace('\"', '\'')

                # otherResource generation
                other_resource_file = os.path.join(resource_dir, '{0}OtherResource.py'.format(str_format_convert(
                    table_dict[table].get('tableName')
                )))
                otherResource_list = self.other_resource_codegen(table_dict[table]).replace('\"', '\'')

                # file write
                loggings.info(1, 'Generating {0}Resource'.format(table_dict[table].get('tableName')))
                file_write(init_file, init_list)
                file_write(urls_file, urls_list)
                file_write(resource_file, resource_list)
                file_write(other_resource_file, otherResource_list)

        except Exception as e:
            loggings.error(1, str(e))
            return

    # init generation
    def init_codegen(self, table):
        try:
            # remove underline
            blueprint_name = str_format_convert(table.get('tableName'))
            # template generation
            blueprint_str = CodeBlockTemplate.init_blueprint.format(blueprint_name.lower(), blueprint_name)
            return FileTemplate.init.format(blueprint=blueprint_str)
        except Exception as e:
            loggings.error(1, str(e))
            return

    #  urls generation
    def urls_codegen(self, table):
        try:
            # remove underline
            api_name = str_format_convert(table.get('tableName'))
            # template  generation
            import_str = CodeBlockTemplate.urls_imports.format(api_name.lower(), Settings.API_VERSION, api_name,
                                                               api_name.capitalize())

            api_str = CodeBlockTemplate.urls_api.format(api_name.lower())

            primary_key_str = CodeBlockTemplate.primary_key.format(
                api_name, str_format_convert(table.get('primaryKey')))
            resource_str = CodeBlockTemplate.urls_resource.format(api_name.capitalize(), primary_key_str, api_name)

            other_resource_str = CodeBlockTemplate.urls_other_resource.format(api_name.capitalize(), api_name, api_name)

            return FileTemplate.urls.format(
                imports=import_str, api=api_str, resource=resource_str, otherResource=other_resource_str)
        except Exception as e:
            loggings.error(1, str(e))
            return

    # resource generation
    def resource_codegen(self, table):
        try:
            # remove underline
            api_name = str_format_convert(table.get('tableName'))
            className_str = api_name[0].upper() + api_name[1:]

            # template  generation
            imports_str = CodeBlockTemplate.resource_imports.format(api_name, className_str)

            id_str = table.get('primaryKey')

            # get field list (except primary key)
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
        except Exception as e:
            loggings.error(1, str(e))
            return

    # otherResource generation
    def other_resource_codegen(self, table):
        try:
            # remove underline
            api_name = str_format_convert(table.get('tableName'))
            className_str = api_name[0].upper() + api_name[1:]

            # template generation
            imports_str = CodeBlockTemplate.resource_imports.format(api_name, className_str)

            id_str = table.get('primaryKey')

            # get field list (except primary key)
            argument_str = ''
            for j in table.get('columns').values():
                if j.get('name') != table.get('primaryKey'):
                    argument_str += CodeBlockTemplate.parameter.format(j.get('name'), j.get('type'))

            getControllerInvoke_str = CodeBlockTemplate.get_controller_invoke.format(className_str)

            postControllerInvoke_str = CodeBlockTemplate.other_resource_post_controller_invoke.format(className_str)

            return FileTemplate.other_resource.format(imports=imports_str, className=className_str, id=id_str,
                                                      argument=argument_str,
                                                      getControllerInvoke=getControllerInvoke_str,
                                                      postControllerInvoke=postControllerInvoke_str
                                                      )
        except Exception as e:
            loggings.error(1, str(e))
            return

    # app_init generation
    def app_codegen(self, app_dir, tables):
        try:
            # app_init
            blueprint_register_str = ''
            for table in tables:
                table_name = str_format_convert(tables[str(table)].get('tableName'))
                blueprint_name = table_name.lower()
                blueprint_register_str += CodeBlockTemplate.app_init_blueprint.format(
                    table_name, Settings.API_VERSION, blueprint_name,
                )
            # print(blueprint_register_str)
            app_init_file = os.path.join(app_dir, '__init__.py')
            new_file_or_dir(1, app_init_file)
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_init.format(blueprint_register=blueprint_register_str))

            # app_setting
            app_setting_file = os.path.join(app_dir, 'setting.py')
            new_file_or_dir(1, app_setting_file)
            with open(app_setting_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_setting)
        except Exception as e:
            loggings.error(1, str(e))



