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

from codegen import project_dir
from .codegenerator import CodeGenerator


def main(table_dict):
    """
    Generate Controller code
    :return: None
    """

    # create the controller file
    os.makedirs(controller_dir := os.path.join(project_dir, 'controller'), exist_ok=True)

    generator = CodeGenerator(table_dict)
    generator.controller_codegen(
        controller_dir=controller_dir
    )
    return
