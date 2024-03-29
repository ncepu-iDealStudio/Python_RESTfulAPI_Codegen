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

from utils.checkSqlLink import SQLHandler
from utils.interface_limiter import InterfaceLimiter

app = Flask(__name__, static_folder="../static")
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效

limiter = InterfaceLimiter.get_limiter(app)


@app.route('/', methods=['GET'])
@limiter.exempt()
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
    database = kwargs['DatabaseName']
    username = kwargs['Username']
    password = parse.quote_plus(kwargs['Password'])

    # 检查数据库链接
    result_sql = SQLHandler.connection_check(dialect, username, password, host, port, database)
    if result_sql['code']:
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功'}
    else:
        return {'code': '4000', 'data': [], 'message': '数据库连接失败'}


# 获取表名
@app.route('/next', methods=['POST'])
def next():
    # 获取会话id并创建对应配置文件
    id = session.get('id')
    ip = request.remote_addr
    dir = os.getcwd()
    f = open(dir + "/config/config_" + str(id) + ".conf", "w")
    f.close()

    # 接收参数
    kwargs = json.loads(request.data)
    dialect = kwargs['DatabaseDialects']
    host = kwargs['Host']
    port = kwargs['Port']
    database = kwargs['DatabaseName']
    username = kwargs['Username']
    password = kwargs['Password']
    # 检查数据库链接
    result_sql = SQLHandler.connect_sql_link(dialect, username, password, host, port, database, id, ip)
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

        return {'code': '2000', 'message': '数据库连接成功'}
    else:
        return {'code': '4000', 'message': result_sql['message']}


# 获取表中字段等信息
@app.route('/next-tables', methods=['GET'])
def next_get_tables():
    # 获取会话id并创建对应配置文件
    id = session.get('id')
    ip = request.remote_addr

    result_sql = SQLHandler.generate_tables_information(id, ip)
    if result_sql['code']:
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功', 'invalid': result_sql['invalid']}
    else:
        return {'code': '4000', 'data': [], 'message': result_sql['message']}


# 获取视图中字段信息
@app.route('/next-views', methods=['GET'])
def next_get_views():
    # 获取会话id并创建对应配置文件
    id = session.get('id')
    ip = request.remote_addr

    result_sql = SQLHandler.generate_views_information(id, ip)
    if result_sql['code']:
        return {'code': '2000', 'data': result_sql['data'], 'message': '数据库连接成功'}
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
    ip = request.remote_addr
    kwargs = json.loads(request.data)
    from codegenerate.main import start
    res = start(kwargs, id, ip)
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
    retval = os.getcwd()
    os.chdir(path)  # 改变工作目录至dist

    zfile = zipfile.ZipFile(folder_dir, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(folder):
        fpath = dirpath.replace(folder, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            zfile.write(os.path.join(dirpath, filename), fpath + filename)
    zfile.close()
    os.chdir(retval)  # 改变工作目录至上一层
    dir = os.getcwd()
    return send_from_directory(os.path.join(dir, "dist"), folder_dir, as_attachment=True)
