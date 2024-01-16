#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:test_checkSqlLink.py
# author:JackieX
# datetime:2024-01-14 17:04
# software: PyCharm
"""
this is function  description 
"""

from sqlalchemy import create_engine, MetaData, inspect
from config.setting import Settings
from utils.checkSqlLink import SQLHandler

if __name__ == '__main__':
    # 参数初始化

    # 替换为你自己的数据库连接字符串
    DATABASE_URI = 'mysql+pymysql://dev:123456@39.99.146.111:13306/study_flask_api'

    # 创建数据库引擎
    engine = create_engine(DATABASE_URI, echo=True)

    # 创建Metadata对象
    metadata = MetaData()

    SQLHandler.engine = engine

    metadata.reflect(schema='study_flask_api', bind=engine)

    SQLHandler.metadata = metadata
    SQLHandler.inspector = inspect(SQLHandler.engine)
    SQLHandler.table_names = SQLHandler.inspector.get_table_names()
    SQLHandler.views_names = SQLHandler.inspector.get_view_names()
    url=SQLHandler.engine.url


    # 测试第一个方法---pass
    # res1 = SQLHandler.connect_sql_link('mysql','dev', '123456', '39.99.146.111','13306', 'study_flask_api')
    #
    # print(res1)

    # 测试第二个方法---pass
    # res2 = SQLHandler.connection_check('mysql', 'dev', '123456', '39.99.146.111', '13306', 'study_flask_api')
    #
    # print(res2)

    # 测试第三个方法
    # res3 = SQLHandler.generate_tables_information()
    #
    # print(res3)
    #
    # # 测试第四个方法
    # res4 = SQLHandler.generate_views_information()
    #
    # print(res4)






    '''
    以下是metadata对象和inspect对象在sqlalchemy 2.0.25下的用法测试；
    '''

    # reflect 映射dash_base库下的表结构
    # metadata.reflect(schema='study_flask_api', bind=engine)
    #
    # tables_info = {i.name: i for i in metadata.tables.values()}
    #
    # print("tables_info :\n", tables_info)
    #
    # insp 创建方式一 推荐
    # insp = inspect(engine)
    # insp 创建方式二 该方式将被移除
    # insp = reflection.Inspector.from_engine(engine)

    # schema_names = insp.get_schema_names()
    # print("schema_names :\n", schema_names)
    # table_names = insp.get_table_names(schema='study_flask_api')  # schema: 数据库名称
    # print("table_names :\n", table_names)
    # columns = insp.get_columns('student', schema='study_flask_api')  # 表名，库名
    # print("table_columns :\n", columns)
