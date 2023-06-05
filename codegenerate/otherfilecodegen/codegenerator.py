#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqlacodegen.py
# author:PigKnight
# datetime:2021/8/23 8:45
# software: PyCharm

"""
  generate other lay code.
"""

import os

from codegenerate.otherfilecodegen.template.filetemplate import FileTemplate
from utils.loggings import loggings

project_dir = ''
api_version = ''
session_id = None
ip = None


class CodeGenerator(object):

    def __init__(self, settings, sessionid, user_ip):
        super(CodeGenerator, self).__init__()
        global project_dir, api_version, session_id, ip
        project_dir = settings.PROJECT_DIR
        api_version = settings.API_VERSION
        session_id = sessionid
        ip = user_ip
        self.maps = {'str': 'string', 'int': 'integer', 'obj': 'object', 'float': 'float'}

    # other file layer generation
    def other_file_generator(self, app_dir, table_dict):

        try:
            # manage.py generation
            self.manage_codegen(table_dict)

            # app/__init__.py generation
            app_init_file = os.path.join(app_dir, '__init__.py')
            with open(app_init_file, 'w', encoding='utf8') as f:
                f.write(FileTemplate.app_init.format(api_version=api_version))

        except Exception as e:
            loggings.exception(1, e, session_id, ip)
            return

    # manage generation
    def manage_codegen(self, tables):
        # permission generation
        permission = ["apiversion.Apiversion"]
        for table in tables.values():
            table_name_little_camel_case = table.get('table_name_little_camel_case')
            table_name_big_camel_case = table.get('table_name_big_camel_case')
            table_name_endpoint = table_name_little_camel_case + '.' + table_name_big_camel_case

            if table.get('is_view'):
                permission.append(table_name_endpoint + 'Query')
            else:
                permission.append(table_name_endpoint)

        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, 'manage.py'), 'w', encoding='utf8') as f:
            f.write(FileTemplate.manage.format(permission=permission))
