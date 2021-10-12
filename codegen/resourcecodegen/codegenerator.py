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

from codegen import project_dir, table_dict
from codegen.resourcecodegen.template.codeblocktemplate import CodeBlockTemplate
from codegen.resourcecodegen.template.filetemplate import FileTemplate
from config.setting import Settings
from utils.common import str_format_convert, new_file_or_dir, file_write
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self):
        super(CodeGenerator, self).__init__()
        self.maps = {'str': 'string', 'int': 'integer', 'obj': 'object', 'float': 'float'}

    # resource layer generation
    def resource_generator(self, api_dir, app_dir):

        # reload settings
        Settings.reload()

        try:
            self.manage_codegen(table_dict)
            # api_init generation
            with open(api_init := os.path.join(api_dir, '__init__.py'), 'w', encoding='utf8') as f:
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
                f.write(FileTemplate.api_version_urls.format(apiversion=Settings.API_VERSION))
            with open(os.path.join(apiVersion_dir, 'apiVersionResource.py'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.api_version_resource.format(
                    apiversion=Settings.API_VERSION.replace('_', '.')))
            os.makedirs(apiVersion_ymls_dir := os.path.join(apiVersion_dir, 'ymls'), exist_ok=True)
            with open(os.path.join(apiVersion_ymls_dir, 'apiversion_get.yml'), 'w', encoding='utf8') as f:
                f.write(FileTemplate.yml_get_template.format('apiversion', ''))

            # file generation
            for table in table_dict.keys():
                os.makedirs(resource_dir := os.path.join(api_dir, '{0}Resource'.format(str_format_convert(
                    table_dict[table].get('table_name')
                ))), exist_ok=True)

                # init generation
                with open(os.path.join(resource_dir, '__init__.py'), 'w', encoding='utf8') as f:
                    f.write(self.init_codegen(table_dict[table]).replace('\"', '\''))

                # urls generation
                with open(os.path.join(resource_dir, 'urls.py'), 'w', encoding='utf8') as f:
                    f.write(self.urls_codegen(table_dict[table]).replace('\"', '\''))

                # resource generation
                with open(os.path.join(resource_dir, '{0}Resource.py'.format(str_format_convert(
                        table_dict[table].get('table_name')
                ))), 'w', encoding='utf8') as f:
                    f.write(self.resource_codegen(table_dict[table]).replace('\"', '\''))

                # otherResource generation
                with open(os.path.join(resource_dir, '{0}OtherResource.py'.format(str_format_convert(
                        table_dict[table].get('table_name')
                ))), 'w', encoding='utf8') as f:
                    f.write(self.other_resource_codegen(table_dict[table]).replace('\"', '\''))

                # ymls generation
                os.makedirs(ymls_dir := os.path.join(resource_dir, 'ymls'), exist_ok=True)
                with open(os.path.join(ymls_dir, '{0}'.format(str_format_convert(
                        table_dict[table].get('table_name'))) + '_get.yml'), 'w', encoding='utf8') as f:
                    f.write(self.yml_get_codegen(table_dict[table]).replace('\"', '\''))
                with open(os.path.join(ymls_dir, '{0}'.format(str_format_convert(
                        table_dict[table].get('table_name'))) + '_gets.yml'), 'w', encoding='utf8') as f:
                    f.write(self.yml_gets_codegen(table_dict[table]).replace('\"', '\''))
                with open(os.path.join(ymls_dir, '{0}'.format(str_format_convert(
                        table_dict[table].get('table_name'))) + '_post.yml'), 'w', encoding='utf8') as f:
                    f.write(self.yml_post_codegen(table_dict[table]).replace('\"', '\''))
                with open(os.path.join(ymls_dir, '{0}'.format(str_format_convert(
                        table_dict[table].get('table_name'))) + '_put.yml'), 'w', encoding='utf8') as f:
                    f.write(self.yml_put_codegen(table_dict[table]).replace('\"', '\''))
                with open(os.path.join(ymls_dir, '{0}'.format(str_format_convert(
                        table_dict[table].get('table_name'))) + '_delete.yml'), 'w', encoding='utf8') as f:
                    f.write(FileTemplate.yml_delete_template.format(table_dict[table].get('table_name')))
        except Exception as e:
            loggings.exception(1, e)
            return

    # init generation
    def init_codegen(self, table):
        try:
            # remove underline
            blueprint_name = str_format_convert(table.get('table_name'))

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
            api_name = str_format_convert(table.get('table_name'))
            className_str = api_name[0].upper() + api_name[1:]

            # template  generation
            import_str = CodeBlockTemplate.urls_imports.format(api_name.lower(), Settings.API_VERSION, api_name,
                                                               className_str)

            api_str = CodeBlockTemplate.urls_api.format(api_name.lower())

            if table.get('business_key'):
                primary_key_str = CodeBlockTemplate.primary_key.format(api_name,
                                                                       table.get('business_key').get('column'))
            else:
                primary_key_str = CodeBlockTemplate.primary_key.format(
                    api_name, str_format_convert(table.get('primaryKey')))

            resource_str = CodeBlockTemplate.urls_resource.format(className_str, primary_key_str, api_name)

            other_resource_str = CodeBlockTemplate.urls_other_resource.format(className_str, api_name)

            service_resource_str = CodeBlockTemplate.urls_service_resource.format(api_name.lower(), api_name,
                                                                                  className_str)
            return FileTemplate.urls.format(
                imports=import_str, api=api_str, resource=resource_str, otherResource=other_resource_str,
                serviceResource=service_resource_str)
        except Exception as e:
            loggings.exception(1, e)
            return

    # resource generation
    def resource_codegen(self, table):
        try:
            # remove underline
            api_name = str_format_convert(table.get('table_name'))
            className_str = api_name[0].upper() + api_name[1:]

            # template  generation
            imports_str = CodeBlockTemplate.resource_imports.format(api_name, className_str)

            if table.get('business_key'):
                id_str = table.get('business_key').get('column')
            else:
                id_str = table.get('primaryKey')

            # get field list (except primary key)
            parameter_post = ''
            parameter_gets = ''
            for column in table.get('columns').values():
                if column.get('name') != table.get('primaryKey') and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter_gets += CodeBlockTemplate.parameter_form_false.format(column.get('name'),
                                                                                   column.get('type'))
                    parameter_post += CodeBlockTemplate.parameter_form_true.format(column.get('name'),
                                                                                   column.get('type'))

            idCheck_str = CodeBlockTemplate.resource_id_check.format(id_str)

            getControllerInvoke_str = CodeBlockTemplate.resource_get_controller_invoke.format(className_str)

            deleteControllerInvoke_str = CodeBlockTemplate.resource_delete_controller_invoke.format(className_str)

            putControllerInvoke_str = CodeBlockTemplate.resource_put_controller_invoke.format(className_str)

            getsControllerInvoke_str = CodeBlockTemplate.resource_gets_controller_invoke.format(className_str)

            postControllerInvoke_str = CodeBlockTemplate.resource_post_controller_invoke.format(className_str)

            return FileTemplate.resource.format(imports=imports_str,
                                                apiName=api_name,
                                                className=className_str,
                                                id=id_str,
                                                idCheck=idCheck_str,
                                                putParameter=parameter_gets,
                                                getsParameter=parameter_gets,
                                                postParameter=parameter_post,
                                                getControllerInvoke=getControllerInvoke_str,
                                                deleteControllerInvoke=deleteControllerInvoke_str,
                                                putControllerInvoke=putControllerInvoke_str,
                                                getsControllerInvoke=getsControllerInvoke_str,
                                                postControllerInvoke=postControllerInvoke_str
                                                )
        except Exception as e:
            loggings.exception(1, e)
            return

    # otherResource generation
    def other_resource_codegen(self, table):
        try:
            # remove underline
            api_name = str_format_convert(table.get('table_name'))
            className_str = api_name[0].upper() + api_name[1:]

            # template generation
            imports_str = CodeBlockTemplate.other_resource_imports.format(api_name, className_str)

            if table.get('business_key'):
                id_str = table.get('business_key').get('column')
            else:
                id_str = table.get('primaryKey')

            # get field list (except primary key)
            parameter_query = ''
            for column in table.get('columns').values():
                if column.get('name') != table.get('primaryKey') and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter_query += CodeBlockTemplate.parameter_args.format(column.get('name'),
                                                                               column.get('type'))

            getServiceInvoke_str = CodeBlockTemplate.other_resource_get_service_invoke.format(className_str)

            return FileTemplate.other_resource.format(imports=imports_str,
                                                      apiName=api_name,
                                                      className=className_str,
                                                      id=id_str,
                                                      queryParameter=parameter_query,
                                                      getServiceInvoke=getServiceInvoke_str
                                                      )
        except Exception as e:
            loggings.exception(1, e)
            return

    # app_init generation
    def app_codegen(self, app_dir, tables):
        try:
            # app_init
            blueprint_register_str = '''from api_{0}.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_{0}")\n'''.format(Settings.API_VERSION)
            for table in tables:
                table_name = str_format_convert(tables[str(table)].get('table_name'))
                blueprint_name = table_name.lower()
                blueprint_register_str += CodeBlockTemplate.app_init_blueprint.format(
                    table_name, Settings.API_VERSION, blueprint_name,
                )
            # print(blueprint_register_str)
            app_init_file = os.path.join(app_dir, '__init__.py')
            new_file_or_dir(1, app_init_file)
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_init.format(blueprint_register=blueprint_register_str))

        except Exception as e:
            loggings.exception(1, e)

    # manage generation
    def manage_codegen(self, tables):
        permission = ["apiVersion.apiVersion"]
        for table in tables.values():
            blueprint_name = str_format_convert(table.get('table_name'))
            permission.append(blueprint_name + '.' + blueprint_name)
            permission.append(blueprint_name + '.' + blueprint_name + '_list')
            permission.append(blueprint_name + '.' + blueprint_name + '_query')

        # swagger permission
        permission.append('flasgger.apidocs')
        permission.append('flasgger.static')
        permission.append('flasgger.apispec_1')

        permission_str = FileTemplate.manage.format(permission=permission)
        new_file_or_dir(2, project_dir)
        manage_file = os.path.join(project_dir, 'manage.py')
        file_write(manage_file, permission_str)

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
            if table.get('business_key'):
                if column.get('name') != table.get('primaryKey') and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_get_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])
            else:
                if column.get('name') != table.get('primaryKey'):
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
            if table.get('business_key'):
                if column.get('name') != table.get('primaryKey') and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_post_parameter_template.format(column.get('name'),
                                                                                      self.maps[column.get('type')])
            else:
                if column.get('name') != table.get('primaryKey'):
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
            if table.get('business_key'):
                if column.get('name') != table.get('primaryKey') and column.get('name') != table.get(
                        'business_key').get('column'):
                    parameter += CodeBlockTemplate.yml_put_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])
            else:
                if column.get('name') != table.get('primaryKey'):
                    parameter += CodeBlockTemplate.yml_put_parameter_template.format(column.get('name'),
                                                                                     self.maps[column.get('type')])

        # yml_gets codegen
        yml_gets = FileTemplate.yml_gets_template.format(table.get('table_name'), parameter, data)
        return yml_gets
