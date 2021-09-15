#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/10 7:55
# @Author  : jianghao
# @File    : server.py
# @Software: PyCharm


import ast
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import configparser

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dialect = request.form.get("dialect")
        driver = request.form.get("driver")
        host = request.form.get("host")
        port = request.form.get("port")
        database = request.form.get("database")
        username = request.form.get("username")
        password = request.form.get("password")
        print(dialect, driver, host, port, database, username, password)
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
        return redirect(url_for('table', info=data))
    return render_template("index.html")


@app.route('/table/<info>')
def table(info):
    info = ast.literal_eval(info)
    return render_template("table.html", data=info)


@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        projectPath = request.form.get("projectPath")
        projectName = request.form.get("projectName")
        interfaceVersion = request.form.get("interfaceVersion")

        configfile = "../config/config.conf"
        conf = configparser.ConfigParser()  # 实例类
        conf.read(configfile, encoding='UTF-8')  # 读取配置文件

        conf.set("PARAMETER", "TARGET_DIR", projectPath)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
        conf.set("PARAMETER", "PROJECT_NAME", projectName)
        conf.set("PARAMETER", "API_VERSION", interfaceVersion)
        with open(configfile, "w") as f:
            conf.write(f)
        return redirect(url_for('build'))
    return render_template("project.html")


@app.route('/build', methods=['GET'])
def build():
    return render_template("build.html")


@app.route('/tableinfo/<tableinfo>')
def tableinfo(tableinfo):
    print(tableinfo)
    return redirect(url_for('project'))


if __name__ == '__main__':
    app.run()
