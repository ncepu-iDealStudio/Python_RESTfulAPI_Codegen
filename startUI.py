#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/10 7:55
# @Author  : jianghao
# @File    : server.py
# @Software: PyCharm

import ast
import json
import webbrowser

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import configparser
from utils.checkSqlLink import check_sql_link

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

        # 检查数据库链接
        result_sql = check_sql_link(dialect, driver, username, password, host, port, database)

        if result_sql['code']:
            # 填写配置文件
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
        return render_template("build.html")
    return render_template("project.html")


@app.route('/build', methods=['GET'])
def build():
    from start import start
    start()
    with open('logs/codegen_log.log', "r",encoding="utf-8") as f:
        log_data = f.read()
    return render_template("build.html", log_data=log_data)


@app.route('/tableinfo/<tableinfo>')
def tableinfo(tableinfo):
    info = ast.literal_eval(tableinfo)
    security_configfile = "config/security.conf"
    security_conf = configparser.ConfigParser()  # 实例类
    security_conf.read(security_configfile, encoding='UTF-8')  # 读取配置文件
    security_conf.remove_section("RSA_TABLE_COLUMN")
    security_conf.add_section("RSA_TABLE_COLUMN")

    config_configfile = "config/config.conf"
    config_config = configparser.ConfigParser()  # 实例类
    config_config.read(config_configfile, encoding='UTF-8')  # 读取配置文件

    table_rule = {
        "table_record_delete_logic_way": [
        ],
        "table_business_key_gen_rule": {
        }
    }
    tables_str = ""
    for tableItem in info:
        if tableItem['issave'] == 'true':
            tables_str = tables_str + tableItem['table'] + ","
            config_config.set("MODEL", 'TABLES', tables_str[:-1])
            with open(config_configfile, "w") as f:
                config_config.write(f)
            if tableItem['encrypt'] != []:
                encrypt_str = ""
                for str in tableItem['encrypt']:
                    encrypt_str = encrypt_str + str + ","
                security_conf.set("RSA_TABLE_COLUMN", tableItem['table'], encrypt_str[:-1])
                with open(security_configfile, "w") as f:
                    security_conf.write(f)
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
    webbrowser.open('http://127.0.0.1:5000')
    app.run()
