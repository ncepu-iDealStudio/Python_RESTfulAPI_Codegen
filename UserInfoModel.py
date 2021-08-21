# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    AutoID = Column(INTEGER(11), primary_key=True, comment=' 主键 自动递增')
    UserID = Column(INTEGER(11), nullable=False, comment='业务主键 用户ID')
    UserName = Column(String(20), nullable=False, comment='用户姓名')
    CreateTime = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    IsDelete = Column(TINYINT(4), server_default=text("'0'"), comment='是否删除  0--没有删除  1 -- 已经删除')
