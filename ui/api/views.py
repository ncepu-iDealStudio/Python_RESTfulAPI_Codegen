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
import os
import time
import zipfile
from datetime import timedelta

import pymysql
from flask import Flask, request, session, send_from_directory
from urllib import parse

from utils.checkSqlLink import check_sql_link, connection_check

app = Flask(__name__, static_folder="../static")
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效


@app.route('/', methods=['GET'])
def index():
    session['id'] = int(round(time.time() * 1000))
    return app.send_static_file('index.html')


@app.route('/tables', methods=['GET'])
def tables():
    return app.send_static_file('tables.html')


@app.route('/views', methods=['GET'])
def views():
    return app.send_static_file('views.html')


@app.route('/tables_info', methods=['GET'])
def tables_info():
    return app.send_static_file('tables_info.html')


@app.route('/project', methods=['GET'])
def project():
    return app.send_static_file('project.html')


@app.route('/build', methods=['GET'])
def build():
    return app.send_static_file('build.html')


# 获取项目路径
@app.route('/getpath', methods=['POST'])
def getpath():
    dir = os.getcwd()
    path = dir + "\dist"
    return {'code': '2000', 'data': path, 'message': '获取路径成功'}


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
    password = parse.quote_plus(kwargs['Password'])

    # 检查数据库链接
    result_sql = connection_check(dialect, username, password, host, port, database)
    if result_sql['code']:
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功'}
    else:
        return {'code': '4000', 'data': [], 'message': '数据库连接失败'}


# 连接数据库接口
@app.route('/next', methods=['POST'])
def next():
    # 获取会话id并创建对应配置文件
    id = session.get('id')
    dir = os.getcwd()
    f = open(dir + "/config/config_" + str(id) + ".conf", "w")
    f.close()

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
        configfile = "config/config_" + str(id) + ".conf"
        conf = configparser.ConfigParser()  # 实例类
        conf.read(configfile, encoding='UTF-8')  # 读取配置文件

        if not conf.has_section('DATABASE'):
            conf.add_section('DATABASE')

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
        return {'code': '4000', 'data': [], 'message': result_sql['message']}


# 完成项目配置
@app.route('/setproject', methods=['POST'])
def setproject():
    kwargs = json.loads(request.data)
    projectPath = 'dist'
    projectName = kwargs["projectName"]
    interfaceVersion = kwargs["projectVersion"]

    id = session.get('id')

    configfile = "config/config_" + str(id) + ".conf"
    conf = configparser.ConfigParser()  # 实例类
    conf.read(configfile, encoding='UTF-8')  # 读取配置文件

    if not conf.has_section('PARAMETER'):
        conf.add_section('PARAMETER')

    conf.set("PARAMETER", "target_dir", projectPath)  # 第一个参数为组名，第二个参数为属性名，第三个参数为属性的值
    conf.set("PARAMETER", "project_name", projectName)
    conf.set("PARAMETER", "api_version", interfaceVersion)
    with open(configfile, "w") as f:
        conf.write(f)
    return {'code': '2000', 'data': [], 'message': '写入配置成功'}


# 开始生成代码
@app.route('/startbuild', methods=['POST'])
def startbuild():
    id = session.get('id')
    kwargs = json.loads(request.data)
    from codegen.main import start
    res = start(kwargs, id)
    if res['code'] == '2000':
        return {'code': '2000', 'data': res['data'], 'message': '目标代码生成成功'}
    else:
        return {'code': '5000', 'data': [], 'message': res['error']}


# 下载
@app.route('/download', methods=['GET'])
def download():
    id = session.get('id')
    path = "dist"
    folder = "dist_" + str(id)
    folder_dir = folder + ".zip"
    os.chdir(path)

    zfile = zipfile.ZipFile(folder_dir, 'w', zipfile.ZIP_DEFLATED)
    for foldername, subfolders, files in os.walk(folder):  # 遍历文件夹

        # 处理根目录不被压缩
        folderoath = foldername.replace(folder, "")
        folderoath = folderoath and folderoath + os.sep or ''

        for i in files:
            zfile.write(os.path.join(foldername, i), folderoath + i)
    dir = os.getcwd()
    return send_from_directory(dir, folder_dir, as_attachment=True)
