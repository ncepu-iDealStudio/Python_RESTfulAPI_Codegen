#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start.py.py
# author:jianghao
# datetime:2021/8/22 16:28
# software: PyCharm

"""
    project start
"""

# from ui.api.views import app
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
