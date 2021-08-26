#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/26 10:58
# software: PyCharm

"""
    this is function description
"""

from codegen.servicecodegen.codegenerator import CodeGenerator
from utils.loggings import loggings
from . import metadata, service_path


def serviceGenerate():
    """
    Generate service layer code
    :return: None
    """
    try:
        generator = CodeGenerator(metadata)
        generator.service_generator(service_path)
    except Exception as e:
        loggings.error(1, str(e))
