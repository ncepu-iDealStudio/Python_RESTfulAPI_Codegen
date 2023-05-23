#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:read_yaml.py
# author:Triblew
# datetime:2022/4/8 19:21
# software: PyCharm

"""
    this is function description
"""

import yaml


def read_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value
