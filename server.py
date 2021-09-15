#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/10 7:55
# @Author  : jianghao
# @File    : server.py
# @Software: PyCharm


import ast
import json
from dataclasses import replace

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import configparser
from utils.checkTable import CheckTable

app = Flask(__name__, template_folder="UI/templates", static_folder="UI/static")
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

        configfile = "config/database.conf"
        conf = configparser.ConfigParser()  # 实例类
        conf.read(configfile, encoding='UTF-8')  # 读取配置文件

        conf.set("DEFAULT", "DIALECT", dialect)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
        conf.set("DEFAULT", "DRIVER", driver)
        conf.set("DEFAULT", "HOST", host)
        conf.set("DEFAULT", "PORT", port)
        conf.set("DEFAULT", "DATABASE", database)
        conf.set("DEFAULT", "USERNAME", username)
        conf.set("DEFAULT", "PASSWORD", password)
        with open(configfile, "w") as f:
            conf.write(f)

        result_sql = CheckTable.check_sql_link()
        if result_sql['code']:
            return redirect(url_for('table', info=result_sql['data']))
        else:
            return render_template("index.html", message=result_sql['message'])
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

        configfile = "config/config.conf"
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
    info = ast.literal_eval(tableinfo)
    configfile = "config/security.conf"
    conf = configparser.ConfigParser()  # 实例类
    conf.read(configfile, encoding='UTF-8')  # 读取配置文件
    conf.remove_section("RSA_TABLE_COLUMN")
    conf.add_section("RSA_TABLE_COLUMN")

    table_rule = {
        "table_record_delete_logic_way": [
        ],
        "table_business_key_gen_rule": {
        }
    }
    for tableItem in info:
        if tableItem['issave'] == 'true':
            if tableItem['encrypt'] != []:
                encrypt_str = ""
                for str in tableItem['encrypt']:
                    encrypt_str = encrypt_str + str + ","
                conf.set("RSA_TABLE_COLUMN", tableItem['table'], encrypt_str[:-1])
                with open(configfile, "w") as f:
                    conf.write(f)
            if tableItem['isdeleted'] == 'true':
                table_rule['table_record_delete_logic_way'].append(tableItem['table'])
            if tableItem['isbusinesskey'] != '':
                table_rule['table_business_key_gen_rule'][tableItem['table']] = {
                    tableItem['isbusinesskey']: tableItem['businesskeyrule']}
    table_rule_json = json.dumps(table_rule)
    with open("config/table_rule.json", "w") as f:
        f.write(table_rule_json)
    return redirect(url_for('project'))


if __name__ == '__main__':
    app.run()
