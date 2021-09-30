#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkSqlLink.py
# author:吴凯博
# datetime:2021/9/16 12:20
# software: PyCharm
"""
this is function description
"""
# import module your need


# 检验数据库连接是否成功并返回所有表、字段信息（前端用）
from sqlalchemy import create_engine, MetaData


def check_sql_link(dialect, driver, username, password, host, port, database):
    """
    检验数据库连接是否成功并返回所有表、字段信息（前端用）
    :param dialect: 数据库种类
    :param driver: 数据库驱动
    :param username: 用户名
    :param password: 密码
    :param host: 数据库IP
    :param port: 数据库端口号
    :param database: 要连接的数据库
    :return code: 布尔型，True表示连接成功，False表示连接失败
    :return message: 返回信息
    :return error: 错误信息
    :return data: 所有表的信息及字段
    """
    try:
        url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(dialect, driver, username, password, host, port, database)
        engine = create_engine(url)
        metadata = MetaData(engine)
        metadata.reflect(engine)
    except Exception as e:
        return {'code': False, 'message': '数据库连接失败', 'error': str(e)}

    data = []
    for table in metadata.tables.values():
        filed = []
        for column in table.columns.values():
            filed.append(str(column).split('.')[-1])
        data.append({
            'table': str(table.name),
            'issave': '',
            'isdeleted': '',
            'filed': filed,
            'encrypt': [],
            'isbusinesskey': '',
            'businesskeyrule': ''
        })
    return {'code': True, 'message': '数据库连接成功', 'data': data}
