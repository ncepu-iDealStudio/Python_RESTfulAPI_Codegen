#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/10 7:55
# @Author  : jianghao
# @File    : server.py
# @Software: PyCharm
from urllib.parse import urlparse, urljoin

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("表单提交成功")
        print(request.form)
        return redirect(url_for('table'))
    return render_template("index.html")


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        print("表单提交成功22")
        print(request.form)
        return redirect(url_for('project'))
    data = [
        {
            'table': "user",
            'issave': '',
            'isdeleted': '',
            'filed': ['autoid', 'name'],
            'encrypt': [],
            'isbusinesskey': '',
            'businesskeyrule': ''
        },
        {
            'table': "userinfo",
            'issave': '',
            'isdeleted': '',
            'filed': ['autoid', 'name', 'userinfo', 'hello', 'world', 'username', 'isdeleted', 'hhhh'],
            'encrypt': [],
            'isbusinesskey': '',
            'businesskeyrule': ''
        }
    ]
    return render_template("table.html", data=data)


@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        print("表单提交成功33")
        print(request.form)
        return redirect(url_for('build'))
    return render_template("project.html")

@app.route('/build', methods=['GET'])
def build():
    return render_template("build.html")


if __name__ == '__main__':
    app.run()
