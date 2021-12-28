#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start.py.py
# author:jianghao
# datetime:2021/8/22 16:28
# software: PyCharm

"""
    project start
"""

import webbrowser
from ui.api.views import app

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run()
