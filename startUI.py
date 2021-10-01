#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/10 7:55
# @Author  : jianghao
# @File    : server.py
# @Software: PyCharm


import webbrowser
from ui.api.views import app

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run()
