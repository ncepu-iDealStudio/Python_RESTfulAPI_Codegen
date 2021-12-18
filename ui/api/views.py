#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:views.py
# author:jianghao
# datetime:2021/9/28 15:21
# software: PyCharm

"""
    this is function description
"""

import ast
import json
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import configparser
from utils.checkSqlLink import check_sql_link

app = Flask(__name__, static_folder="../static")


# 新的vue接口

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/tables', methods=['GET'])
def tables():
    return app.send_static_file('tables.html')


@app.route('/tables_info', methods=['GET'])
def tables_info():
    return app.send_static_file('tables_info.html')


@app.route('/project', methods=['GET'])
def project():
    return app.send_static_file('project.html')


@app.route('/build', methods=['GET'])
def build():
    return app.send_static_file('build.html')


# 连接数据库接口
@app.route('/connect', methods=['POST'])
def connect():
    # 接收参数
    kwargs = json.loads(request.data)
    dialect = kwargs['DatabaseDialects']
    driver = kwargs['Driver']
    host = kwargs['Host']
    port = kwargs['Port']
    database = kwargs['DatebaseName']
    username = kwargs['Username']
    password = kwargs['Password']
    # tables 置为为空
    configfile = "config/config.conf"
    conf = configparser.ConfigParser()
    conf.read(configfile, encoding='UTF-8')
    conf.set("MODEL", "TABLES", '')
    with open(configfile, "w") as f:
        conf.write(f)
    # 检查数据库链接
    result_sql = check_sql_link(dialect, driver, username, password, host, port, database)
    if result_sql['code']:
        global tabledata
        tabledata = result_sql['data']
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
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功'}
    else:
        return {'code': '4000', 'data': [], 'message': '数据库连接失败'}


# 完成表配置
@app.route('/settables', methods=['POST'])
def settables():
    tabledata = json.loads(request.data)
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
    for tableItem in tabledata:
        if tableItem['issave']:
            tables_str = tables_str + tableItem['table'] + ","
            config_config.set("MODEL", 'TABLES', tables_str[:-1])
            with open(config_configfile, "w") as f:
                config_config.write(f)

            if tableItem['isdeleted']:
                table_rule['table_record_delete_logic_way'].append(tableItem['table'])

            if tableItem['isbusinesskey'] != '':
                table_rule['table_business_key_gen_rule'][tableItem['table']] = {
                    tableItem['isbusinesskey']: tableItem['businesskeyrule']}

            for i in tableItem['filed']:
                encrypt_str = ""
                encrypt_str = encrypt_str + i['field_name'] + ","
                security_conf.set("RSA_TABLE_COLUMN", tableItem['table'], encrypt_str[:-1])
                with open(security_configfile, "w") as f:
                    security_conf.write(f)

    table_rule_json = json.dumps(table_rule)
    with open("config/table_rule.json", "w") as f:
        f.write(table_rule_json)
    return {'code': '2000', 'data': [], 'message': '写入配置成功'}


# 完成项目配置
@app.route('/setproject', methods=['POST'])
def setproject():
    kwargs = json.loads(request.data)
    projectPath = kwargs["projectPath"]
    projectName = kwargs["projectName"]
    interfaceVersion = kwargs["projectVersion"]

    configfile = "config/config.conf"
    conf = configparser.ConfigParser()  # 实例类
    conf.read(configfile, encoding='UTF-8')  # 读取配置文件

    conf.set("PARAMETER", "TARGET_DIR", projectPath)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
    conf.set("PARAMETER", "PROJECT_NAME", projectName)
    conf.set("PARAMETER", "API_VERSION", interfaceVersion)
    with open(configfile, "w") as f:
        conf.write(f)
    return {'code': '2000', 'data': [], 'message': '写入配置成功'}


# 开始生成代码
@app.route('/startbuild', methods=['POST'])
def startbuild():
    from codegen.main import start
    try:
        start()
        with open('logs/codegen_log.log', "r", encoding="utf-8") as f:
            log_data = f.read()
        return {'code': '2000', 'data': log_data, 'message': '写入配置成功'}
    except Exception as e:
        return {'code': '5000', 'data': [], 'message': '生成失败'}


# 关闭服务
@app.route('/seriouslykill', methods=['POST'])
def seriouslykill():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {'code': '2000', 'data': [], 'message': 'http://127.0.0.1:5000/ is shutdown!'}


# 解决跨域
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://admin.writer..quwancode.com':
            response.headers["Access-Control-Allow-Origin"] = 'http://admin.writer.quwancode.com'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response
