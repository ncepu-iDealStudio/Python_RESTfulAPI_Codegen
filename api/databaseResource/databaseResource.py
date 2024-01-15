#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:databaseResource.py
# author:jackiex
# datetime:2024/1/15 15:12
# software: PyCharm

'''
    数据库信息获取与操作相关接口
'''

import json
import keyword

from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base

from utils.response_code import RET
from utils.loggings import loggings


class DatabaseResource(Resource):
    def __init__(self, dialect: str, host: str, port: int, database: str, username: str, password: str):
        # 创建数据库连接字符串
        connection_string = f"{dialect}://{username}:{password}@{host}:{port}/{database}"

        # 创建数据库引擎
        self.engine = create_engine(connection_string)

        # 获取元数据
        self.metadata = automap_base()
        self.metadata.prepare(self.engine, reflect=True)

        # 获取表和视图名称列表
        self.inspector = inspect(self.engine)
        self.table_names = self.inspector.get_table_names()
        self.views_names = self.inspector.get_view_names()

    @classmethod
    def db_conn_test(cls):
        # 接收参数
        kwargs = json.loads(request.data)
        dialect = kwargs['DatabaseDialects']
        host = kwargs['Host']
        port = kwargs['Port']
        database = kwargs['DatabaseName']
        username = kwargs['Username']
        password = kwargs['Password']
        try:
            driver_dict = {
                'mysql': 'pymysql',
                'mssql': 'pymssql',
                'oracle': 'cx_oracle',
                'postgresql': 'psycopg2'
            }
            url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(dialect, driver_dict[dialect], username, password, host,
                                                               port, database)
            engine = create_engine(url)
            metadata = MetaData(engine)
            metadata.reflect(engine)
            return {'code': RET.ok, 'message': '数据库连接成功', 'data': ''}
        except Exception as e:
            return {'code': RET.DBERR, 'message': '数据库连接失败', 'error': str(e)}

    # get all database names of a database server
    @classmethod
    def get_database_names(cls):
        # 接收参数
        kwargs = json.loads(request.data)
        dialect = kwargs['DatabaseDialects']
        host = kwargs['Host']
        port = kwargs['Port']
        username = kwargs['Username']
        password = kwargs['Password']
        try:
            driver_dict = {
                'mysql': 'pymysql',
                'mssql': 'pymssql',
                'oracle': 'cx_oracle',  # oracle需要安装cx_oracle
                'postgresql': 'psycopg2'
            }
            url = '{}+{}://{}:{}@{}:{}/'.format(dialect, driver_dict[dialect], username, password, host, port)
            engine = create_engine(url)
            conn = engine.connect()
            result = conn.execute('SELECT name FROM sys.databases;')
            data = result.fetchall()
            data_list = []
            for i in data:
                data_list.append(i[0])
            return {'code': RET.ok, 'message': '数据库连接成功', 'data': data_list}
        except Exception as e:
            return {'code': RET.DBERR, 'message': '数据库连接失败', 'error': str(e)}

    # get all tables name in database
    @classmethod
    def get_tables_names(cls):
        # 接收参数
        kwargs = json.loads(request.data)
        dialect = kwargs['DatabaseDialects']
        host = kwargs['Host']
        port = kwargs['Port']
        username = kwargs['Username']
        password = kwargs['Password']
        database = kwargs['Database']
        try:
            driver_dict = {
                'mysql': 'pymysql',
                'mssql': 'pymssql',   # mssql需要安装pymssql
                'sqlite': 'sqlite3',
                'postgresql': 'psycopg2'
            }
            url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'\
                .format(dialect, driver_dict[dialect], username, password, host, port, database)
            engine = create_engine(url)
            metadata = MetaData(engine)
            tables = metadata.tables.keys()
            return {'code': RET.ok, 'message': '数据库连接成功', 'data': tables}
        except Exception as e:
            return {'code': RET.DBERR, 'message': '数据库连接失败', 'error': str(e)}


    # Define a method to check if all tables in this database contain primary keys;
    # Return two lists (with and without primary keys)
    def get_tables_with_pk(self,session_id, ip):
       # 获取所有的表
        tables = self.get_tables_names()
        if tables['code'] != RET.ok:
            return tables
        else:
            tables_with_pk = []
            tables_without_pk = []
            for table in tables['data']:
                # 获取表的元数据
                table_metadata = self.metadata.tables[table]
                # 获取表的主键
                table_pk = table_metadata.primary_key
                # 如果表的主键不为空，说明这个表有主键
                if table_pk:
                    tables_with_pk.append(table)
                # 如果表的主键为空，说明这个表没有主键
                else:
                    tables_without_pk.append(table)
                    loggings.warning(1, 'table {0} do not have a primary key'.format(table['table_name']), session_id,
                                     ip)
            return {'code': RET.ok, 'message': '获取表的主键成功', 'data': {'tables_with_pk': tables_with_pk, 'tables_without_pk': tables_without_pk}}

    # check contains keywords of python in tables or in its  columns
    # return a list of tables or columns which contains keywords
    def check_keywords_in_tables_or_columns(self,session_id, ip):
        # 获取所有的表
        tables = self.get_tables_names()
        if tables['code'] != RET.ok:
            return tables
        else:
            available_table = []
            invalid_table = []

            for table in tables.values():

                flag = True

                # 检查表名是否为python关键字
                if keyword.iskeyword(table['table_name']):
                    loggings.warning(1, 'table "{0}" is a keyword of python'.format(table['table_name']), session_id,
                                     ip)
                    flag = False

                for column in table['columns'].values():
                    # 检查表字段是否为python关键字
                    if keyword.iskeyword(column['name']):
                        loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table['table_name'],
                                                                                             column['name']),
                                         session_id,
                                         ip)
                        flag = False

                if flag:
                    available_table.append(table['table_name'])
                else:
                    invalid_table.append(table['table_name'])

            return available_table, invalid_table

    # check if the table is empty
    # return a list of tables which is empty
    def check_empty_tables(self ,tables):
        # 定义一个列表，用于存储空表
        empty_tables = []
        for table in tables:
            # 获取表的元数据
            table_metadata = self.metadata.tables[table]
            # 获取表的列
            columns = table_metadata.columns
            # 获取表的数据
            table_data = self.engine.execute(table_metadata.select()).fetchall()
            # 如果表的数据为空，说明这个表是空表
            if len(table_data) == 0:
                empty_tables.append(table)
        return {'code': RET.ok, 'message': '获取空表成功', 'data': empty_tables}
