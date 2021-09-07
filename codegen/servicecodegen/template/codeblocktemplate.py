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

    service_import = """import math

from app import db
from controller.{table_name}Controller import {table_name_initials_upper}Controller
from models.{table_name}Model import {table_name_initials_upper}{foreign_import}
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
"""

    single_filter_condition = """            if kwargs.get('{colums_name}'):
                filter_list.append(cls.{colums_name} == kwargs.get('{colums_name}'))
"""

    join_statement = '.join({target_table}, {table_name_initials_upper}.{table_key} == {target_table}.{target_key})'
    exception_return = "{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}"
    notdata_return = "{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}"
    success_return = "{'code': RET.OK, 'message': error_map_EN[RET.OK], 'count': count, 'pages': pages, 'data': results}"
