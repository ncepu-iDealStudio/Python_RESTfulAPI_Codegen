#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:Triblew
# datetime:2022/4/8 19:31
# software: PyCharm

"""
    启动主入口
"""

import os

if __name__ == '__main__':
    command = "locust --config=config/locust.conf"
    os.system(command)
