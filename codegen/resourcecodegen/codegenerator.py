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

from codegen.resourcecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.resourcecodegen.template.filetemplate import FileTemplate
from utils.loggings import loggings

project_dir = ''
api_version = ''
session_id = None


class CodeGenerator(object):

    def __init__(self, settings, sessionid):
        super(CodeGenerator, self).__init__()
        global project_dir, api_version, session_id
        project_dir = settings.PROJECT_DIR
        api_version = settings.API_VERSION
        session_id = sessionid
        self.maps = {'str': 'string', 'int': 'integer', 'obj': 'object', 'float': 'float'}

    # resource layer generation
    def resource_generator(self, api_dir, app_dir, table_dict):

        try:
            # table_dict processing
            for table in table_dict.keys():
                if table_dict[table]['is_view']:
                    pass
                else:
                    table_dict[table]['autoincrement_columns'] = []
                    table_dict[table]['nullable_columns'] = []
                    table_dict[table]['exist_default_columns'] = []
                    table_dict[table]['post_columns'] = {}
                    table_dict[table]['delete_columns'] = {}
                    table_dict[table]['put_columns'] = {}
                    table_dict[table]['get_columns'] = {}
                    for column in table_dict[table]['columns'].values():
                        if column['is_autoincrement']:
                            table_dict[table]['autoincrement_columns'].append(column.get('name'))
                        if column['nullable']:
                            table_dict[table]['nullable_columns'].append(column.get('name'))
                        if column['is_exist_default']:
                            table_dict[table]['exist_default_columns'].append(column.get('name'))
                        rsa_columns = table_dict[table]['rsa_columns']
                        if len(table_dict[table].get('primary_key_columns')) > 1:
                            if column.get('name') in table_dict[table].get('primary_key_columns'):
                                table_dict[table]['post_columns'][column.get('name')] = True
                                table_dict[table]['put_columns'][column.get('name')] = True
                                table_dict[table]['delete_columns'][column.get('name')] = True
                            else:
                                table_dict[table]['post_columns'][column.get('name')] = False
                                table_dict[table]['put_columns'][column.get('name')] = False
                            if column.get('name') not in rsa_columns:
                                table_dict[table]['get_columns'][column.get('name')] = False
                        else:
                            business_key = table_dict[table].get('business_key_column').get('column')
                            business_key_rule = table_dict[table].get('business_key_column').get('rule')
                            primary_key = table_dict[table].get('primary_key_columns')[0]
                            delete_column = table_dict[table].get('logical_delete_column') or ''
                            # real primary key
                            if business_key:
                                real_primary_key = business_key
                            else:
                                real_primary_key = primary_key
                            table_dict[table]['real_primary_key'] = real_primary_key

                            if column.get('name') == business_key and business_key_rule:
                                continue
                            elif column.get('name') == primary_key and primary_key != business_key:
                                continue
                            elif column.get('name') == delete_column:
                                continue
                            else:
                                if column.get('name') not in rsa_columns and column.get('nullable'):
                                    table_dict[table]['post_columns'][column.get('name')] = False
                                # 不是null且有默认值，则非必填
                                elif column.get('is_exist_default'):
                                    table_dict[table]['post_columns'][column.get('name')] = False
                                # 不是null且无默认值，则必填
                                else:
                                    table_dict[table]['post_columns'][column.get('name')] = True
                                if column.get('name') != real_primary_key:
                                    if column.get('name') not in rsa_columns:
                                        table_dict[table]['get_columns'][column.get('name')] = False
                                    table_dict[table]['put_columns'][column.get('name')] = False
                                    table_dict[table]['delete_columns'][column.get('name')] = False

            # manage.py generation
            self.manage_codegen(table_dict)

            # api/__init__.py generation
            with open(os.path.join(api_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(self.api_codegen(table_dict))

            # app/__init__.py generation
            app_init_file = os.path.join(app_dir, '__init__.py')
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_init.format(api_version=api_version))

            # api/apiVersionResource/* generation
            os.makedirs(apiVersion_dir := os.path.join(api_dir, 'apiVersionResource'), exist_ok=True)

            with open(os.path.join(apiVersion_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_init)

            with open(os.path.join(apiVersion_dir, 'urls.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_urls.format(apiversion=api_version))

            with open(os.path.join(apiVersion_dir, 'apiVersionResource.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_resource.format(apiversion=api_version.replace('_', '.')))

            # file generation
            for table in table_dict.values():
                table_name_little_camel_case = table.get('table_name_little_camel_case')
                os.makedirs(resource_dir := os.path.join(api_dir, '{0}Resource'.format(table_name_little_camel_case)),
                            exist_ok=True)

                # init generation
                with open(os.path.join(resource_dir, '__init__.py'), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen(table))

                # urls generation
                with open(os.path.join(resource_dir, 'urls.py'), 'w', encoding='utf8') as f:
                    f.write(self.urls_codegen(table))

                # resource generation
                if not table.get('is_view'):
                    with open(os.path.join(resource_dir, '{0}Resource.py'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(self.resource_codegen(table))

                # otherResource generation
                with open(os.path.join(resource_dir, '{0}OtherResource.py'.format(table_name_little_camel_case)),
                          'w', encoding='utf8') as f:
                    f.write(self.other_resource_codegen(table))

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    # init generation
    def init_codegen(self, table):
        try:
            table_name_all_small = table.get('table_name_all_small')
            table_name_little_camel_case = table.get('table_name_little_camel_case')

            return FileTemplate.init.format(
                table_name_all_small=table_name_all_small,
                table_name_little_camel_case=table_name_little_camel_case).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    #  urls generation
    def urls_codegen(self, table):
        try:
            table_name_all_small = table.get('table_name_all_small')
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')
            table_name_api_standard = table.get('table_name_api_standard')

            if table.get('is_view'):
                import_str = CodeBlockTemplate.urls_imports_view.format(table_name_all_small,
                                                                        api_version,
                                                                        table_name_little_camel_case,
                                                                        table_name_big_camel_case)
                other_resource_str = CodeBlockTemplate.urls_other_resource.format(table_name_all_small,
                                                                                  table_name_api_standard,
                                                                                  table_name_big_camel_case)
                return FileTemplate.urls_view.format(imports=import_str,
                                                     table_name_all_small=table_name_all_small,
                                                     otherResource=other_resource_str
                                                     ).replace('\"', '\'')
            else:
                import_str = CodeBlockTemplate.urls_imports_table.format(table_name_all_small,
                                                                         api_version,
                                                                         table_name_little_camel_case,
                                                                         table_name_big_camel_case)

                if table.get('business_key_column').get('column'):
                    primary_key_str = CodeBlockTemplate.primary_key_single.format(table_name_little_camel_case,
                                                                                  table.get('business_key_column').get(
                                                                                      'column'))
                else:
                    if len(table.get('primary_key_columns')) > 1:
                        primary_key_str = CodeBlockTemplate.primary_key_multi.format(table_name_little_camel_case)
                    else:
                        primary_key_str = CodeBlockTemplate.primary_key_single.format(
                            table_name_api_standard, table.get('primary_key_columns')[0])

                resource_str = CodeBlockTemplate.urls_resource.format(table_name_big_camel_case, primary_key_str)

                return FileTemplate.urls.format(imports=import_str,
                                                table_name_all_small=table_name_all_small,
                                                resource=resource_str
                                                ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    # resource generation
    def resource_codegen(self, table):
        try:
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')

            # get field list (except primary key)
            parameter_post = ''
            parameter_get = ''
            parameter_put = ''
            parameter_delete = ''

            # multiple primary key
            if len(table.get('primary_key_columns')) > 1:
                for column in table.get('columns').values():
                    column_name = column.get('name')
                    if column_name in table.get('post_columns').keys():
                        parameter_post += CodeBlockTemplate.parameter_3.format(
                            column=column_name,
                            location='form',
                            required=table.get('post_columns').get(column_name)
                        )
                    if column_name in table.get('delete_columns'):
                        parameter_delete += CodeBlockTemplate.parameter_2.format(
                            column=column_name,
                            location='form',
                            required=table.get('delete_columns').get(column_name)
                        )
                    if column_name in table.get('put_columns'):
                        parameter_put += CodeBlockTemplate.parameter_2.format(
                            column=column_name,
                            location='form',
                            required=table.get('put_columns').get(column_name)
                        )
                    if column_name in table.get('get_columns'):
                        parameter_get += CodeBlockTemplate.parameter_2.format(
                            column=column_name,
                            location='args',
                            required=table.get('get_columns').get(column_name)
                        )

                return FileTemplate.resource_multi_primary_key.format(
                    table_name_little_camel_case=table_name_little_camel_case,
                    table_name_big_camel_case=table_name_big_camel_case,
                    apiName=table_name_little_camel_case,
                    className=table_name_big_camel_case,
                    putParameter=parameter_put,
                    getParameter=parameter_get,
                    postParameter=parameter_post,
                    deleteParameter=parameter_delete
                ).replace('\"', '\'')
            # single primary key
            else:
                for column in table.get('columns').values():
                    column_name = column.get('name')
                    if column_name in table.get('post_columns').keys():
                        parameter_post += CodeBlockTemplate.parameter_3.format(
                            column=column_name,
                            location='form',
                            required=table.get('post_columns').get(column_name)
                        )
                    if column_name in table.get('delete_columns'):
                        parameter_delete += CodeBlockTemplate.parameter_3.format(
                            column=column_name,
                            location='form',
                            required=table.get('delete_columns').get(column_name)
                        )
                    if column_name in table.get('put_columns'):
                        parameter_put += CodeBlockTemplate.parameter_2.format(
                            column=column_name,
                            location='form',
                            required=table.get('put_columns').get(column_name)
                        )
                    if column_name in table.get('get_columns'):
                        parameter_get += CodeBlockTemplate.parameter_2.format(
                            column=column_name,
                            location='args',
                            required=table.get('get_columns').get(column_name)
                        )

                id_str = table.get('real_primary_key')

                return FileTemplate.resource.format(
                    table_name_little_camel_case=table_name_little_camel_case,
                    table_name_big_camel_case=table_name_big_camel_case,
                    apiName=table_name_little_camel_case,
                    className=table_name_big_camel_case,
                    id=id_str,
                    putParameter=parameter_put,
                    getParameter=parameter_get,
                    postParameter=parameter_post,
                    deleteParameter=parameter_delete
                ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    # otherResource generation
    def other_resource_codegen(self, table):
        try:
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')

            parameter = ''
            method = '\tpass'

            if table.get('is_view'):
                imports_str = CodeBlockTemplate.other_resource_imports.format(table_name_little_camel_case,
                                                                              table_name_big_camel_case)
                for column in table.get('columns'):
                    parameter += CodeBlockTemplate.parameter_2.format(
                        column=column.get('field_name'),
                        location='args',
                        required='False'
                    )
                method = CodeBlockTemplate.other_resource_query.format(parameter, table_name_big_camel_case)
            else:
                imports_str = ""

            return FileTemplate.other_resource.format(
                imports=imports_str,
                className=table_name_big_camel_case,
                method=method
            ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    # api_init generation
    def api_codegen(self, tables):
        try:
            imports_str = '''from .apiVersionResource import apiversion_blueprint\n'''
            blueprint_register_str = '''    from api_{0}.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_{0}")\n'''.format(api_version)

            for table in tables.values():
                table_name_all_small = table.get('table_name_all_small')
                table_name_little_camel_case = table.get('table_name_little_camel_case')

                imports_str += CodeBlockTemplate.api_init_imports.format(
                    table_name_little_camel_case, table_name_all_small
                )
                blueprint_register_str += CodeBlockTemplate.api_init_blueprint.format(
                    table_name_little_camel_case, api_version, table_name_all_small,
                )

            return FileTemplate.api_init.format(
                imports=imports_str,
                blueprint_register=blueprint_register_str)

        except Exception as e:
            loggings.exception(1, e, session_id)
            return

    # manage generation
    def manage_codegen(self, tables):
        # permission generation
        permission = ["apiversion.apiversion"]
        for table in tables.values():
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_endpoint = table_name_little_camel_case + '.' + table_name_little_camel_case

            if table.get('is_view'):
                permission.append(table_name_endpoint + '_query')
            else:
                permission.append(table_name_endpoint)

        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, 'manage.py'), 'w', encoding='utf8') as f:
            f.write(FileTemplate.manage.format(permission=permission))
