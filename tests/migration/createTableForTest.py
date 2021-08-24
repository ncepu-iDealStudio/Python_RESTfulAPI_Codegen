#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:createTableForTest.py
# author:jackiex
# datetime:2021/8/24 16:36
# software: PyCharm

'''
    创建默认的数据库和表，用于测试
'''
from sqlalchemy import Column
from sqlalchemy.engine import create_engine
from sqlalchemy.types import Integer, String, Date, Float

conn_url = 'mysql://root:123456@127.0.0.1:3306/testlogin?charset=utf8'
engine = create_engine(conn_url,encoding='utf-8',echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)

#数据库的模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(length=8), unique=True)
    pwd = Column(String(length=3))
    birth = Column(Date)
    score = Column(Float(decimal_return_scale=2))


if __name__ == '__main__':
    Base.metadata.create_all()
    #Base.metadata.drop_all()
