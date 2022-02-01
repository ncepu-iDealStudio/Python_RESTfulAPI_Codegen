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
from utils.common import str_to_all_small, str_to_little_camel_case, str_to_big_camel_case
from utils.loggings import loggings

project_dir = ''
api_version = ''
flasgger_mode = ''


class CodeGenerator(object):

    def __init__(self, settings):
        super(CodeGenerator, self).__init__()
        global project_dir, api_version, flasgger_mode
        project_dir = settings.PROJECT_DIR
        api_version = settings.API_VERSION
        flasgger_mode = settings.FLASGGER_MODE
        self.maps = {'str': 'string', 'int': 'integer', 'obj': 'object', 'float': 'float'}

    # resource layer generation
    def resource_generator(self, api_dir, app_dir, table_dict):

        try:
            # table_dict processing
            for table in table_dict.keys():
                table_dict[table]['table_name_all_small'] = str_to_all_small(table)
                table_dict[table]['table_name_little_camel_case'] = str_to_little_camel_case(table)
                table_dict[table]['table_name_big_camel_case'] = str_to_big_camel_case(table)
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
                        if len(table_dict[table].get('primaryKey')) > 1:
                            if column.get('name') in table_dict[table].get('primaryKey'):
                                table_dict[table]['post_columns'][column.get('name')] = True
                                table_dict[table]['put_columns'][column.get('name')] = True
                                table_dict[table]['delete_columns'][column.get('name')] = True
                            else:
                                table_dict[table]['post_columns'][column.get('name')] = False
                                table_dict[table]['put_columns'][column.get('name')] = False
                            if column.get('name') not in rsa_columns:
                                table_dict[table]['get_columns'][column.get('name')] = False
                        else:
                            business_key = table_dict[table].get('business_key').get('column')
                            business_key_rule = table_dict[table].get('business_key').get('rule')
                            primary_key = table_dict[table].get('primaryKey')[0]
                            delete_column = table_dict[table].get('logical_delete_mark') or ''
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
                f.write('#!/usr/bin/env python \n# -*- coding:utf-8 -*-')

            # app/__init__.py generation
            loggings.info(1, 'Start generating API layer, please wait...')
            app_init_file = os.path.join(app_dir, '__init__.py')
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(self.app_codegen(table_dict))
            loggings.info(1, 'Generating API layer complete')

            # api/apiVersionResource/* generation
            os.makedirs(apiVersion_dir := os.path.join(api_dir, 'apiVersionResource'), exist_ok=True)

            with open(os.path.join(apiVersion_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_init)

            with open(os.path.join(apiVersion_dir, 'urls.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_urls.format(apiversion=api_version))

            with open(os.path.join(apiVersion_dir, 'apiVersionResource.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_resource.format(apiversion=api_version.replace('_', '.')))

            # apiversion ymls file generation
            if flasgger_mode:
                os.makedirs(apiVersion_ymls_dir := os.path.join(apiVersion_dir, 'ymls'), exist_ok=True)
                with open(os.path.join(apiVersion_ymls_dir, 'apiversion_get.yml'), 'w', encoding='utf8') as f:
                    f.write(FileTemplate.yml_get_template.format('apiversion', ''))

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

                # ymls generation
                if flasgger_mode and not table.get('is_view'):
                    os.makedirs(ymls_dir := os.path.join(resource_dir, 'ymls'), exist_ok=True)
                    with open(os.path.join(ymls_dir, '{0}_get.yml'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(self.yml_get_codegen(table))

                    with open(os.path.join(ymls_dir, '{0}_gets.yml'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(self.yml_gets_codegen(table))

                    with open(os.path.join(ymls_dir, '{0}_post.yml'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(self.yml_post_codegen(table))

                    with open(os.path.join(ymls_dir, '{0}_put.yml'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(self.yml_put_codegen(table))

                    with open(os.path.join(ymls_dir, '{0}_delete.yml'.format(table_name_little_camel_case)),
                              'w', encoding='utf8') as f:
                        f.write(FileTemplate.yml_delete_template.format(table.get('table_name')))

        except Exception as e:
            loggings.exception(1, e)
            return

    # init generation
    def init_codegen(self, table):
        try:
            table_name_all_small = table.get('table_name_all_small')
            table_name_little_camel_case = table.get('table_name_little_camel_case')

            blueprint_str = CodeBlockTemplate.init_blueprint.format(table_name_all_small,
                                                                    table_name_little_camel_case)

            return FileTemplate.init.format(blueprint=blueprint_str).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e)
            return

    #  urls generation
    def urls_codegen(self, table):
        try:
            table_name_all_small = table.get('table_name_all_small')
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')

            import_str = CodeBlockTemplate.urls_imports.format(table_name_all_small,
                                                               api_version,
                                                               table_name_little_camel_case,
                                                               table_name_big_camel_case)

            if table.get('is_view'):
                import_str = CodeBlockTemplate.urls_imports_view.format(table_name_all_small,
                                                                        api_version,
                                                                        table_name_little_camel_case,
                                                                        table_name_big_camel_case)
                other_resource_str = CodeBlockTemplate.urls_service_resource.format(table_name_all_small,
                                                                                    table_name_little_camel_case,
                                                                                    table_name_big_camel_case)
                return FileTemplate.urls_view.format(imports=import_str,
                                                     otherResource=other_resource_str
                                                     ).replace('\"', '\'')
            else:
                api_str = CodeBlockTemplate.urls_api.format(table_name_all_small)
                if table.get('business_key').get('column'):
                    primary_key_str = CodeBlockTemplate.primary_key.format(table_name_little_camel_case,
                                                                           table.get('business_key').get('column'))
                else:
                    if len(table.get('primaryKey')) > 1:
                        primary_key_str = CodeBlockTemplate.primary_key_multi.format(table_name_little_camel_case)
                    else:
                        primary_key_str = CodeBlockTemplate.primary_key.format(
                            table_name_little_camel_case, table.get('primaryKey')[0])

                resource_str = CodeBlockTemplate.urls_resource.format(table_name_big_camel_case, primary_key_str,
                                                                      table_name_little_camel_case)

                return FileTemplate.urls.format(imports=import_str,
                                                api=api_str,
                                                resource=resource_str
                                                ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e)
            return

    # resource generation
    def resource_codegen(self, table):
        try:
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')

            imports_str = CodeBlockTemplate.resource_imports.format(table_name_little_camel_case,
                                                                    table_name_big_camel_case)

            # get field list (except primary key)
            parameter_post = ''
            parameter_get = ''
            parameter_put = ''
            parameter_delete = ''

            # swag generation
            if flasgger_mode:
                swag_get = CodeBlockTemplate.resource_swag_get.format(table_name_little_camel_case)
                swag_put = CodeBlockTemplate.resource_swag_put.format(table_name_little_camel_case)
                swag_post = CodeBlockTemplate.resource_swag_post.format(table_name_little_camel_case)
                swag_delete = CodeBlockTemplate.resource_swag_delete.format(table_name_little_camel_case)

                import_flasgger = CodeBlockTemplate.resource_import_flasgger
            else:
                swag_get = ''
                swag_put = ''
                swag_post = ''
                swag_delete = ''

                import_flasgger = ''

            # multiple primary key
            if len(table.get('primaryKey')) > 1:
                for column in table.get('columns').values():
                    column_name = column.get('name')
                    if column_name in table.get('post_columns').keys():
                        if table.get('post_columns').get(column_name):
                            parameter_post += CodeBlockTemplate.parameter_form_true.format(column_name)
                        else:
                            parameter_post += CodeBlockTemplate.parameter_form_false.format(column_name)
                    if column_name in table.get('delete_columns'):
                        if table.get('delete_columns').get(column_name):
                            parameter_delete += CodeBlockTemplate.parameter_form_true_multi_primary.format(column_name)
                    if column_name in table.get('put_columns'):
                        if table.get('put_columns').get(column_name):
                            parameter_put += CodeBlockTemplate.parameter_form_true_multi_primary.format(column_name)
                        else:
                            parameter_put += CodeBlockTemplate.parameter_form_false_multi_primary.format(column_name)
                    if column_name in table.get('get_columns'):
                        if table.get('get_columns').get(column_name):
                            pass
                        else:
                            parameter_get += CodeBlockTemplate.parameter_args_false_multi_primary.format(column_name)

                return FileTemplate.resource_multi_primary_key.format(
                    swag_get=swag_get,
                    swag_put=swag_put,
                    swag_post=swag_post,
                    swag_delete=swag_delete,
                    imports=imports_str,
                    flasgger_import=import_flasgger,
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
                        if table.get('post_columns').get(column_name):
                            parameter_post += CodeBlockTemplate.parameter_form_true.format(column_name)
                        else:
                            parameter_post += CodeBlockTemplate.parameter_form_false.format(column_name)
                    if column_name in table.get('delete_columns'):
                        if table.get('delete_columns').get(column_name):
                            pass
                        else:
                            parameter_delete += CodeBlockTemplate.parameter_form_delete_false.format(column_name)
                    if column_name in table.get('put_columns'):
                        if table.get('put_columns').get(column_name):
                            pass
                        else:
                            parameter_put += CodeBlockTemplate.parameter_form_put_false.format(column_name)
                    if column_name in table.get('get_columns'):
                        if table.get('get_columns').get(column_name):
                            pass
                        else:
                            parameter_get += CodeBlockTemplate.parameter_args.format(column_name)

                id_str = table.get('real_primary_key')

                return FileTemplate.resource.format(
                    swag_get=swag_get,
                    swag_put=swag_put,
                    swag_post=swag_post,
                    swag_delete=swag_delete,
                    imports=imports_str,
                    flasgger_import=import_flasgger,
                    apiName=table_name_little_camel_case,
                    className=table_name_big_camel_case,
                    id=id_str,
                    putParameter=parameter_put,
                    getParameter=parameter_get,
                    postParameter=parameter_post,
                    deleteParameter=parameter_delete
                ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e)
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
                    parameter += CodeBlockTemplate.parameter_args_joint.format(column.get('field_name'))
                method = CodeBlockTemplate.other_resource_query.format(parameter, table_name_big_camel_case)
            else:
                imports_str = ""

            return FileTemplate.other_resource.format(
                imports=imports_str,
                className=table_name_big_camel_case,
                method=method
            ).replace('\"', '\'')

        except Exception as e:
            loggings.exception(1, e)
            return

    # app_init generation
    def app_codegen(self, tables):
        try:
            # app_init
            blueprint_register_str = '''from api_{0}.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_{0}")\n'''.format(api_version)

            for table in tables.values():
                table_name_all_small = table.get('table_name_all_small')
                table_name_little_camel_case = table.get('table_name_little_camel_case')

                blueprint_register_str += CodeBlockTemplate.app_init_blueprint.format(
                    table_name_little_camel_case, api_version, table_name_all_small,
                )

            return FileTemplate.app_init.format(blueprint_register=blueprint_register_str)

        except Exception as e:
            loggings.exception(1, e)
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

        # swagger permission
        permission.append('flasgger.apidocs')
        permission.append('flasgger.static')
        permission.append('flasgger.apispec_1')
        permission.append('flasgger.<lambda>')

        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, 'manage.py'), 'w', encoding='utf8') as f:
            f.write(FileTemplate.manage.format(permission=permission))

    # yml generation
    def yml_get_codegen(self, table):
        # data codegen
        data = ""
        for column in table.get('columns').values():
            data += CodeBlockTemplate.yml_data_template.format(column.get('name'), self.maps[column.get('type')])

        # yml_get codegen
        yml_get = FileTemplate.yml_get_template.format(table.get('table_name'), data).replace('\"', '\'')
        return yml_get

    def yml_gets_codegen(self, table):
        # data codegen
        data = ""
        parameter = ""
        for column in table.get('columns').values():
            data += CodeBlockTemplate.yml_data_template.format(column.get('name'), self.maps[column.get('type')])
            if table.get('business_key').get('column'):
                if column.get('name') != table.get('primaryKey')[0] and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_get_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])

            else:
                if column.get('name') != table.get('primaryKey')[0]:
                    parameter += CodeBlockTemplate.yml_get_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])

        # yml_gets codegen
        yml_gets = FileTemplate.yml_gets_template.format(table.get('table_name'), parameter, data).replace('\"', '\'')
        return yml_gets

    def yml_post_codegen(self, table):
        # data codegen
        data = ""
        parameter = ""
        for column in table.get('columns').values():
            data += CodeBlockTemplate.yml_data_template.format(column.get('name'), self.maps[column.get('type')])
            if table.get('business_key').get('column'):
                if column.get('name') != table.get('primaryKey')[0] and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_post_parameter_template.format(column.get('name'),
                                                                                      self.maps[column.get('type')])

            else:
                if column.get('name') != table.get('primaryKey')[0]:
                    parameter += CodeBlockTemplate.yml_post_parameter_template.format(column.get('name'),
                                                                                      self.maps[column.get('type')])

        # yml_post codegen
        yml_post = FileTemplate.yml_post_template.format(table.get('table_name'), parameter, data).replace('\"', '\'')
        return yml_post

    def yml_put_codegen(self, table):
        # data codegen
        data = ""
        parameter = ""
        for column in table.get('columns').values():
            data += CodeBlockTemplate.yml_data_template.format(column.get('name'), self.maps[column.get('type')])
            if table.get('business_key').get('column'):
                if column.get('name') != table.get('primaryKey')[0] and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_put_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])

            else:
                if column.get('name') != table.get('primaryKey')[0]:
                    parameter += CodeBlockTemplate.yml_put_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])

        # yml_gets codegen
        yml_gets = FileTemplate.yml_gets_template.format(table.get('table_name'), parameter, data).replace('\"', '\'')
        return yml_gets
