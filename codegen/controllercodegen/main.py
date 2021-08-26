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

from codegen import codegen_layer, metadata, tables, project_dir, target_dir
from utils.common import new_file_or_dir
from . import record_delete_way
from .codegenerator import CodeGenerator


def controllerGenerate():
    """
    Generate Controller code
    :return: None
    """

    # return, while codegen_layer is not 'default' or 'controller'
    if codegen_layer not in ['default', 'controller']:
        return

    if not tables:
        return

    # create the target dir
    new_file_or_dir(2, target_dir)
    new_file_or_dir(2, project_dir)
    controller_dir = os.path.join(project_dir, 'controller')
    new_file_or_dir(2, controller_dir)

    generator = CodeGenerator(metadata)
    generator.controller_codegen(delete_way=record_delete_way, controller_dir=controller_dir)
    return


if __name__ == '__main__':
    controllerGenerate()
