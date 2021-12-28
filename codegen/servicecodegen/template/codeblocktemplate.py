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

    service_import = """
from controller.{table_name}Controller import {table_name_initials_upper}Controller
"""
