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

from codegen import table_dict, project_dir
from config.setting import Settings
from .codegenerator import CodeGenerator


def main():
    """
    Generate Controller code
    :return: None
    """

    if not table_dict:
        return

    # create the controller file
    os.makedirs(controller_dir := os.path.join(project_dir, 'controller'), exist_ok=True)

    generator = CodeGenerator(table_dict)
    generator.controller_codegen(
        controller_dir=controller_dir,
        logical_delete_mark=Settings.LOGICAL_DELETE_MARK
    )
    return
