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

from config.setting import Settings
from utils.checkTable import CheckTable
from utils.common import new_file_or_dir
from .codegenerator import CodeGenerator
from . import codegen_layer, metadata, record_delete_way


def controllerGenerate():
    """
    Generate Controller code
    :return: None
    """

    # return, while codegen_layer is not 'default' or 'controller'
    if codegen_layer not in ['default', 'controller']:
        return

    tables = CheckTable.check_primary_key()
    if not tables:
        return

    # create the target dir
    new_file_or_dir(2, Settings.TARGET_DIR)
    new_file_or_dir(2, Settings.PROJECT_DIR)
    controller_dir = os.path.join(Settings.PROJECT_DIR, 'controller')
    new_file_or_dir(2, controller_dir)

    generator = CodeGenerator(metadata)
    generator.controller_codegen(delete_way=record_delete_way, controller_dir=controller_dir)
    return


if __name__ == '__main__':
    controllerGenerate()
