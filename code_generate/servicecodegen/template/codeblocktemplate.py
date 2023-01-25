#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codeblocktemplate.py
# author:Nathan
# datetime:2021/8/26 11:16
# software: PyCharm

"""
    Code block template file for service layer code
"""


class CodeBlockTemplate(object):
    """
        Code block template class for service layer code
    """

    service_table_import = """
from controller.{table_name}Controller import {table_name_initials_upper}Controller
"""

    service_view_import = """
import math

from app import db
from models.{view_name} import t_{original_view_name}
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET, error_map_EN
"""

    filter_conditions = """        if kwargs.get('{column}') is not None:
            filter_list.append(t_{original_view_name}.columns['{column}'] == kwargs.get('{column}'))
"""

    filter_conditions_for_str = """        if kwargs.get('{column}'):
            filter_list.append(t_{original_view_name}.columns['{column}'].like("%" + kwargs.get('{column}') + "%"))
"""