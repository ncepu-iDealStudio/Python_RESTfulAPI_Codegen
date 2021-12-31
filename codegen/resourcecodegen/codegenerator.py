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

from codegen import project_dir, api_version, flasgger_mode
from codegen.resourcecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.resourcecodegen.template.filetemplate import FileTemplate
from utils.common import str_to_all_small, str_to_little_camel_case, str_to_big_camel_case
from utils.loggings import loggings
flasgger_mode = True

class CodeGenerator(object):

    def __init__(self):
        super(CodeGenerator, self).__init__()
        self.maps = {'str': 'string', 'int': 'integer', 'obj': 'object', 'float': 'float'}

    # resource layer generation
    def resource_generator(self, api_dir, app_dir, table_dict):

        try:
            self.manage_codegen(table_dict)
            # api_init generation
            with open(os.path.join(api_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write('#!/usr/bin/env python \n# -*- coding:utf-8 -*-')

            # app generation
            loggings.info(1, 'Start generating API layer, please wait...')
            self.app_codegen(app_dir, table_dict)
            loggings.info(1, 'Generating API layer complete')

            # apiVersion file generation
            os.makedirs(apiVersion_dir := os.path.join(api_dir, 'apiVersionResource'), exist_ok=True)

            with open(os.path.join(apiVersion_dir, '__init__.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_init)
            with open(os.path.join(apiVersion_dir, 'urls.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_urls.format(apiversion=api_version))
            with open(os.path.join(apiVersion_dir, 'apiVersionResource.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_resource.format(apiversion=api_version.replace('_', '.')))

            # apiversion ymls file generation
            os.makedirs(apiVersion_ymls_dir := os.path.join(apiVersion_dir, 'ymls'), exist_ok=True)
            with open(os.path.join(apiVersion_ymls_dir, 'apiversion_get.yml'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.yml_get_template.format('apiversion', ''))

            # file generation
            for table in table_dict.keys():
                table_name_small_hump = str_to_little_camel_case(table_dict[table].get('table_name'))
                os.makedirs(resource_dir := os.path.join(api_dir, '{0}Resource'.format(table_name_small_hump)), exist_ok=True)

                # init generation
                with open(os.path.join(resource_dir, '__init__.py'), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen(table_dict[table]).replace('\"', '\''))

                # urls generation
                with open(os.path.join(resource_dir, 'urls.py'), 'w', encoding='utf8') as f:
                    f.write(self.urls_codegen(table_dict[table]).replace('\"', '\''))

                # resource generation
                with open(os.path.join(resource_dir, '{0}Resource.py'.format(table_name_small_hump)), 'w', encoding='utf8') as f:
                    f.write(self.resource_codegen(table_dict[table]).replace('\"', '\''))

                # otherResource generation
                with open(os.path.join(resource_dir, '{0}OtherResource.py'.format(table_name_small_hump)), 'w', encoding='utf8') as f:
                    f.write(self.other_resource_codegen(table_dict[table]).replace('\"', '\''))

                # ymls generation
                if flasgger_mode:
                    os.makedirs(ymls_dir := os.path.join(resource_dir, 'ymls'), exist_ok=True)
                    with open(os.path.join(ymls_dir, '{0}'.format(table_name_small_hump) + '_get.yml'), 'w', encoding='utf8') as f:
                        f.write(self.yml_get_codegen(table_dict[table]).replace('\"', '\''))
                    with open(os.path.join(ymls_dir, '{0}'.format(table_name_small_hump) + '_gets.yml'), 'w', encoding='utf8') as f:
                        f.write(self.yml_gets_codegen(table_dict[table]).replace('\"', '\''))
                    with open(os.path.join(ymls_dir, '{0}'.format(table_name_small_hump) + '_post.yml'), 'w', encoding='utf8') as f:
                        f.write(self.yml_post_codegen(table_dict[table]).replace('\"', '\''))
                    with open(os.path.join(ymls_dir, '{0}'.format(table_name_small_hump) + '_put.yml'), 'w', encoding='utf8') as f:
                        f.write(self.yml_put_codegen(table_dict[table]).replace('\"', '\''))
                    with open(os.path.join(ymls_dir, '{0}'.format(table_name_small_hump) + '_delete.yml'), 'w', encoding='utf8') as f:
                        f.write(FileTemplate.yml_delete_template.format(table_dict[table].get('table_name')))

        except Exception as e:
            loggings.exception(1, e)
            return

    # init generation
    def init_codegen(self, table):
        try:
            # remove underline
            table_name_small_hump = str_to_little_camel_case(table.get('table_name'))
            blueprint_name = table_name_small_hump

            # template generation
            blueprint_str = CodeBlockTemplate.init_blueprint.format(blueprint_name.lower(), blueprint_name)
            return FileTemplate.init.format(blueprint=blueprint_str)

        except Exception as e:
            loggings.exception(1, e)
            return

    #  urls generation
    def urls_codegen(self, table):
        try:
            # remove underline
            table_name_all_small = str_to_all_small(table.get('table_name'))
            table_name_small_hump = str_to_little_camel_case(table.get('table_name'))
            table_name_big_hump = str_to_big_camel_case(table.get('table_name'))

            # template  generation
            import_str = CodeBlockTemplate.urls_imports.format(table_name_all_small, api_version, table_name_small_hump,
                                                               table_name_big_hump)

            api_str = CodeBlockTemplate.urls_api.format(table_name_all_small)

            if table.get('business_key').get('column'):
                primary_key_str = CodeBlockTemplate.primary_key.format(table_name_small_hump,
                                                                       table.get('business_key').get('column'))
            else:
                primary_key_str = CodeBlockTemplate.primary_key.format(
                    table_name_small_hump, table.get('primaryKey')[0])

            resource_str = CodeBlockTemplate.urls_resource.format(table_name_big_hump, primary_key_str, table_name_small_hump)

            return FileTemplate.urls.format(
                imports=import_str, api=api_str, resource=resource_str)

        except Exception as e:
            loggings.exception(1, e)
            return

    # resource generation
    def resource_codegen(self, table):
        try:
            table_name_all_small = str_to_all_small(table.get('table_name'))
            table_name_small_hump = str_to_little_camel_case(table.get('table_name'))
            table_name_big_hump = str_to_big_camel_case(table.get('table_name'))

            # remove underline
            # api_name = table_name_small_hump
            # className_str = api_name[0].upper() + api_name[1:]

            # template  generation
            imports_str = CodeBlockTemplate.resource_imports.format(table_name_small_hump, table_name_big_hump)

            business_key = table.get('business_key').get('column')
            primaryKey = table.get('primaryKey')[0]

            if table.get('logical_delete_mark'):
                delete_column = table.get('logical_delete_mark')
            else:
                delete_column = ''

            # get field list (except primary key)
            parameter_post = ''
            parameter_get = ''
            parameter_put = ''
            parameter_delete = ''
            rsa_columns = table.get('rsa_columns')

            for column in table.get('columns').values():
                if column.get('name') == business_key and table.get('business_key').get('rule'):
                    continue
                elif column.get('name') == primaryKey and primaryKey != business_key:
                    continue
                elif column.get('name') == delete_column:
                    continue
                else:
                    if column.get('name') not in rsa_columns and column.get('nullable'):
                        parameter_post += CodeBlockTemplate.parameter_form_false.format(column.get('name'),
                                                                                        column.get('type'))
                    else:
                        parameter_post += CodeBlockTemplate.parameter_form_true.format(column.get('name'),
                                                                                       column.get('type'))
                    parameter_delete += CodeBlockTemplate.parameter_form_delete_false.format(column.get('name'),
                                                                                             column.get('type'))
                    parameter_get += CodeBlockTemplate.parameter_args.format(column.get('name'), column.get('type'))
                    parameter_put += CodeBlockTemplate.parameter_form_put_false.format(column.get('name'),
                                                                                       column.get('type'))
            if business_key:
                id_str = business_key
            else:
                id_str = primaryKey

            # swag generation
            if flasgger_mode:
                swag_get = CodeBlockTemplate.resource_swag_get.format(table_name_small_hump)
                swag_put = CodeBlockTemplate.resource_swag_put.format(table_name_small_hump)
                swag_post = CodeBlockTemplate.resource_swag_post.format(table_name_small_hump)
                swag_delete = CodeBlockTemplate.resource_swag_delete.format(table_name_small_hump)

                import_flasgger = CodeBlockTemplate.resource_import_flasgger
            else:
                swag_get = ''
                swag_put = ''
                swag_post = ''
                swag_delete = ''

                import_flasgger = ''


            return FileTemplate.resource.format(
                swag_get=swag_get,
                swag_put=swag_put,
                swag_post=swag_post,
                swag_delete=swag_delete,
                imports=imports_str,
                flasgger_import=import_flasgger,
                apiName=table_name_small_hump,
                className=table_name_big_hump,
                id=id_str,
                putParameter=parameter_put,
                getParameter=parameter_get,
                postParameter=parameter_post,
                deleteParameter=parameter_delete
            )

        except Exception as e:
            loggings.exception(1, e)
            return

    # otherResource generation
    def other_resource_codegen(self, table):
        try:
            table_name_all_small = str_to_all_small(table.get('table_name'))
            table_name_small_hump = str_to_little_camel_case(table.get('table_name'))
            table_name_big_hump = str_to_big_camel_case(table.get('table_name'))

            # remove underline
            # api_name = table_name_small_hump
            # className_str = api_name[0].upper() + api_name[1:]

            # template generation
            imports_str = CodeBlockTemplate.other_resource_imports

            return FileTemplate.other_resource.format(
                imports=imports_str,
                className=table_name_big_hump
            )

        except Exception as e:
            loggings.exception(1, e)
            return

    # app_init generation
    def app_codegen(self, app_dir, tables):
        try:
            # app_init
            blueprint_register_str = '''from api_{0}.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_{0}")\n'''.format(api_version)

            for table in tables:
                table_name = str(table)
                table_name_all_small = str_to_all_small(table_name)
                table_name_small_hump = str_to_little_camel_case(table_name)
                table_name_big_hump = str_to_big_camel_case(table_name)

                # table_name = str_format_convert(tables[str(table)].get('table_name'))
                # table_name = table_name_small_hump
                # blueprint_name = table_name_all_small
                blueprint_register_str += CodeBlockTemplate.app_init_blueprint.format(
                    table_name_small_hump, api_version, table_name_all_small,
                )

            # print(blueprint_register_str)
            app_init_file = os.path.join(app_dir, '__init__.py')
            # new_file_or_dir(1, app_init_file)
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_init.format(blueprint_register=blueprint_register_str))

        except Exception as e:
            loggings.exception(1, e)

    # manage generation
    def manage_codegen(self, tables):
        permission = ["apiversion.apiversion"]
        for table in tables.values():
            table_name_all_small = str_to_all_small(table.get('table_name'))
            table_name_small_hump = str_to_little_camel_case(table.get('table_name'))
            table_name_big_hump = str_to_big_camel_case(table.get('table_name'))

            # blueprint_name = table_name_small_hump
            permission.append(table_name_small_hump + '.' + table_name_small_hump)
            permission.append(table_name_small_hump + '.' + table_name_small_hump + '_list')
            permission.append(table_name_small_hump + '.' + table_name_small_hump + '_query')

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
        yml_get = FileTemplate.yml_get_template.format(table.get('table_name'), data)
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
        yml_gets = FileTemplate.yml_gets_template.format(table.get('table_name'), parameter, data)
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
        yml_post = FileTemplate.yml_post_template.format(table.get('table_name'), parameter, data)
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
        yml_gets = FileTemplate.yml_gets_template.format(table.get('table_name'), parameter, data)
        return yml_gets
