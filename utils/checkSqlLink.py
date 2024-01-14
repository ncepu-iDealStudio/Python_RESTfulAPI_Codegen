#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkSqlLink.py
# author:Itsuka
# datetime:2021/9/16 12:20
# software: PyCharm

"""
    检验数据库连接是否成功并返回所有表、字段信息（前端用）
"""
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from urllib import parse

from sqlalchemy import create_engine, inspect, MetaData
from utils.checkTable import CheckTable


class SQLHandler:
    engine = None
    metadata = None
    inspector = None
    table_names = None
    views_names = None


    @classmethod
    def connect_sql_link(cls, dialect, username, password, host, port, database, session_id=None, ip=None):
        """
            数据库连接
            :param dialect: 数据库种类
            :param username: 用户名
            :param password: 密码
            :param host: 数据库IP
            :param port: 数据库端口号
            :param database: 要连接的数据库
            :param session_id: 用户session ID
            :param ip: 用户IP地址
            :return None
        """
        try:
            driver_dict = {
                'mysql': 'pymysql',
                'mssql': 'pymssql',
                'oracle': 'cx_oracle',
                'postgresql': 'psycopg2'
            }
            password = parse.quote_plus(password)
            url = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(dialect, driver_dict[dialect], username, password, host,
                                                               port, database)
            cls.metadata_schema=url
            cls.engine = create_engine(url)

        except Exception as e:
            return {'code': False, 'message': str(e), 'error': str(e)}
        return {'code': True, 'message': '成功'}

    @classmethod
    def connection_check(cls, dialect, username, password, host, port, database) -> dict:
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
            return {'code': True, 'message': '数据库连接成功', 'data': ''}
        except Exception as e:
            return {'code': False, 'message': '数据库连接失败', 'error': str(e)}

    @classmethod
    def generate_tables_information(cls, session_id=None, ip=None) -> dict:
        """返回所有表、字段信息（前端用）

            :param session_id: 用户session ID
            :param ip: 用户IP地址
            :return code: 布尔型，True表示连接成功，False表示连接失败
            :return message: 返回信息
            :return error: 错误信息
            :return data: 所有表的信息及字段
            :return invalid: 检查不通过的表，以列表返还表名
        """
        try:

            cls.metadata = MetaData(cls.engine)
            cls.inspector = inspect(cls.engine)
            cls.table_names = cls.inspector.get_table_names()
            cls.views_names = cls.inspector.get_view_names()

            def metadata_reflection(target_engine, target_metadata, target_name):
                """
                    元数据反射获取
                """
                target_metadata.reflect(target_engine, views=False, only=[target_name])

            pool = ThreadPool(2 * cpu_count() + 1)
            # 生成表元数据
            for table_name in cls.table_names:
                pool.apply_async(metadata_reflection, (cls.engine, cls.metadata, table_name))

            pool.close()
            pool.join()

        except Exception as e:
            return {'code': False, 'message': str(e), 'error': str(e)}

        table_dict, invalid_tables = CheckTable.main(cls.metadata, session_id, ip, cls.views_names)

        data = {
            'table': [],
        }
        for table in table_dict.values():
            # 是一个基本表
            filed = []
            business_key_type = ''
            for column in table['columns'].values():
                if table.get('business_key_column') and column['name'] == table['primary_key_columns'][0]:
                    # 唯一主键不是递增时，需要记录该主键的数据类型
                    business_key_type = column['type']
                if column['name'] in table['primary_key_columns']:
                    # 剔除出主键
                    continue
                else:
                    filed.append({
                        'field_name': column['name'],
                        'field_type': column['type'],
                        'field_encrypt': False
                    })
            data['table'].append({
                'table': str(table['table_name']),
                'businesskeyname': table['business_key_column'].get('column') if table['business_key_column'].get(
                    'column') else '',
                'businesskeyrule': '',
                'logicaldeletemark': '',
                'field': filed,
                'businesskeyuneditable': True if table['business_key_column'].get('column') or len(
                    table['primary_key_columns']) > 1 else False,
                "businesskeytype": business_key_type,
                'issave': False
            })
        return {'code': True, 'message': '成功', 'data': data, 'invalid': invalid_tables}

    @classmethod
    def generate_views_information(cls, session_id=None, ip=None) -> dict:
        """
        返回所有视图、字段信息（前端用）
        :param session_id: 用户session ID
        :param ip: 用户IP地址
        :return code: 布尔型，True表示连接成功，False表示连接失败
        :return message: 返回信息
        :return error: 错误信息
        :return data: 所有的视图信息及字段
        """
        try:
            def metadata_reflection(target_engine, target_metadata, target_name):
                """
                    元数据反射获取
                """
                target_metadata.reflect(target_engine, views=True, only=[target_name])

            pool = ThreadPool(2 * cpu_count() + 1)
            # 生成表元数据
            for view_name in cls.views_names:
                pool.apply_async(metadata_reflection, (cls.engine, cls.metadata, view_name))

            pool.close()
            pool.join()

        except Exception as e:
            return {'code': False, 'message': str(e), 'error': str(e)}

        table_dict = CheckTable.main(cls.metadata,  session_id, ip, cls.views_names, view=True)

        data = {
            'view': []
        }
        for table in table_dict.values():
            filter_field = []
            for column in table['columns']:
                column['ischecked'] = False
                filter_field.append(column)
            data['view'].append({
                'view': table['table_name'],
                'filter_field': filter_field,
                'ischecked': False
            })
        return {'code': True, 'message': '成功', 'data': data}
