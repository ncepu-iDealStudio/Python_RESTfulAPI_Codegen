#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkSqlLink.py
# author:Itsuka
# datetime:2021/9/16 12:20
# software: PyCharm

"""
    检验数据库连接是否成功并返回所有表、字段信息（前端用）
"""

from sqlalchemy import create_engine, MetaData
from utils.checkTable import CheckTable


def check_sql_link(dialect, username, password, host, port, database) -> dict:
    """
    返回所有表、字段信息（前端用）
    :param dialect: 数据库种类
    :param username: 用户名
    :param password: 密码
    :param host: 数据库IP
    :param port: 数据库端口号
    :param database: 要连接的数据库
    :return code: 布尔型，True表示连接成功，False表示连接失败
    :return message: 返回信息
    :return error: 错误信息
    :return data: 所有表的信息及字段
    :return invalid: 检查不通过的表，以列表返还表名
    """
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
    except Exception as e:
        return {'code': False, 'message': str(e), 'error': str(e)}

    table_dict, invalid_tables = CheckTable.main(metadata)

    data = []
    for table in table_dict.values():
        filed = []
        for column in table['columns'].values():
            if str(column['name']) == table['primaryKey'][0]:
                continue
            filed.append({
                'field_name': column['name'],
                'field_type': column['type'],
                'field_encrypt': False
            })
        data.append({
            'table': str(table['table_name']),
            'businesskeyname': '',
            'businesskeyrule': '',
            'logicaldeletemark': '',
            'field': filed,
            'issave': False
        })
    return {'code': True, 'message': '成功', 'data': data, 'invalid': invalid_tables}


def connection_check(dialect, username, password, host, port, database) -> dict:
    """
    检验数据库连接是否成功
    :param dialect: 数据库种类
    :param username: 用户名
    :param password: 密码
    :param host: 数据库IP
    :param port: 数据库端口号
    :param database: 要连接的数据库
    :return code: 布尔型，True表示连接成功，False表示连接失败
    :return message: 返回信息
    :return error: 错误信息
    """
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
        return {'code': True, 'message': '数据库连接成功', 'data':''}
    except Exception as e:
        return {'code': False, 'message': '数据库连接失败', 'error': str(e)}
