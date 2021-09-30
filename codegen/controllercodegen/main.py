#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:Itsuka
# datetime:2021/8/26 14:33
# software: PyCharm

"""
    this is function description
"""
import os

from codegen import codegen_layer, table_dict, project_dir, target_dir
from utils.common import new_file_or_dir
from . import rsa_table_column
from .codegenerator import CodeGenerator


def main():
    """
    Generate Controller code
    :return: None
    """

    # return, while codegen_layer is not 'default' or 'controller'
    if codegen_layer not in ['default', 'controller']:
        return

    if not table_dict:
        return

    # create the target dir
    new_file_or_dir(2, target_dir)
    new_file_or_dir(2, project_dir)
    controller_dir = os.path.join(project_dir, 'controller')
    new_file_or_dir(2, controller_dir)

    generator = CodeGenerator(table_dict)
    generator.controller_codegen(
        controller_dir=controller_dir,
        rsa_table_column=rsa_table_column
    )
    return
