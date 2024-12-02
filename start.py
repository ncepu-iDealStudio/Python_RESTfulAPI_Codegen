#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start1.py
# author:jackiex
# datetime:2020/12/2 15:52
# update_time:2024/12/2 15:52
# software: PyCharm

import webbrowser
from app import app

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run()
