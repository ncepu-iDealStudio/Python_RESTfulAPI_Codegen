#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/26 10:58
# software: PyCharm

"""
    this is function description
"""

import os

from codegen.servicecodegen.codegenerator import CodeGenerator
from utils.loggings import loggings


def main(table_dict, settings):
    """
    Generate service layer code
    :return: None
    """
    try:
        project_dir = settings.PROJECT_DIR

        # Create folder named "service" in project directory
        service_path = os.path.join(project_dir, 'service')
        os.makedirs(service_path, exist_ok=True)
        with open(os.path.join(service_path, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python\n# -*- coding:utf-8 -*-\n")

        generator = CodeGenerator(table_dict)
        generator.service_generator(service_path)
    except Exception as e:
        loggings.exception(1, e)
