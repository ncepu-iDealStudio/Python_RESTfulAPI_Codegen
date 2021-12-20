#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:views.py
# author:jianghao
# datetime:2021/9/28 15:21
# software: PyCharm

"""
    this is function description
"""

import configparser
import json

import pymysql
from flask import Flask, request

from utils.checkSqlLink import check_sql_link, connection_check

app = Flask(__name__, static_folder="../static")


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


# 获取数据库名
@app.route('/getdbname', methods=['POST'])
def getdbname():
    try:
        kwargs = json.loads(request.data)
        conn = pymysql.connect(
            host=kwargs['Host'],
            user=kwargs['Username'],
            passwd=kwargs['Password'],
            port=int(kwargs['Port']),
        )
        cur = conn.cursor()
        cur.execute('SHOW DATABASES')
    except Exception as e:
        return {'code': '4000', 'data': [], 'message': str(e)}
    return {'code': '2000', 'data': cur.fetchall(), 'message': '数据库连接成功'}


# 连接数据库接口
@app.route('/connecttest', methods=['POST'])
def connecttest():
    # 接收参数
    kwargs = json.loads(request.data)
    dialect = kwargs['DatabaseDialects']
    host = kwargs['Host']
    port = kwargs['Port']
    database = kwargs['DatebaseName']
    username = kwargs['Username']
    password = kwargs['Password']
    # 检查数据库链接
    result_sql = connection_check(dialect, username, password, host, port, database)
    if result_sql['code']:
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功'}
    else:
        return {'code': '4000', 'data': [], 'message': '数据库连接失败'}


# 连接数据库接口
@app.route('/connect', methods=['POST'])
def connect():
    # 接收参数
    kwargs = json.loads(request.data)
    dialect = kwargs['DatabaseDialects']
    host = kwargs['Host']
    port = kwargs['Port']
    database = kwargs['DatebaseName']
    username = kwargs['Username']
    password = kwargs['Password']
    # 检查数据库链接
    result_sql = check_sql_link(dialect, username, password, host, port, database)
    if result_sql['code']:
        # 填写配置文件
        configfile = "config/config.conf"
        conf = configparser.ConfigParser()  # 实例类
        conf.read(configfile, encoding='UTF-8')  # 读取配置文件
        conf.set("DATABASE", "dialect", dialect)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
        conf.set("DATABASE", "host", host)
        conf.set("DATABASE", "port", port)
        conf.set("DATABASE", "database", database)
        conf.set("DATABASE", "username", username)
        conf.set("DATABASE", "password", password)
        with open(configfile, "w") as f:
            conf.write(f)
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功', 'invalid': result_sql['invalid']}
    else:
        return {'code': '4000', 'data': [], 'message': '数据库连接失败'}


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

    conf.set("PARAMETER", "target_dir", projectPath)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
    conf.set("PARAMETER", "project_name", projectName)
    conf.set("PARAMETER", "api_version", interfaceVersion)
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
