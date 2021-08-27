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
from utils.response_code import RET
from utils.loggings import loggings
"""

    single_filter_condition = """            if kwargs.get('{colums_name}'):
                filter_list.append(cls.{colums_name} == kwargs.get('{colums_name}'))
"""

    exception_return = "{'code': RET.DBERR, 'message': '数据库异常，获取信息失败', 'error': str(e)}"
    notdata_return = "{'code': RET.NODATA, 'message': '查无信息', 'error': '查无信息'}"
    success_return = "{'code': RET.OK, 'message': '查询成功', 'count': count, 'pages': pages, 'data': results}"
