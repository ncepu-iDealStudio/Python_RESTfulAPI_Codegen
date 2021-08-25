#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkPrimaryKey.py
# author:Itsuka
# datetime:2021/8/25 9:53
# software: PyCharm

"""
    this is function description
"""
from sqlalchemy import create_engine, MetaData
from config.setting import Settings


# 检查table主键
def check_primary_key():
    """
    根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
    :return: 符合规范的表列表，即有且仅有一个自增主键，没有符合规范的情况下返回None
    """
    url = Settings.MODEL_URL
    engine = create_engine(url)
    metadata = MetaData(engine)
    metadata.reflect(engine)
    tables = []
    # 根据代码生成模式获取表列表
    if Settings.CODEGEN_MODE == 'table':
        for i in Settings.MODEL_TABLES.replace(' ', '').split(','):
            tables.append(metadata.tables[i])
    else:
        tables = metadata.tables.values()
    results = []
    for i in tables:
        primary_flag = False  # 有无主键
        autoincrement_flag = False  # 是否自增
        repeat_flag = False  # 主键是否重复
        for j in i.c.values():  # j为字段(Column)
            if j.primary_key is True:
                if not primary_flag:
                    primary_flag = True
                else:
                    repeat_flag = True
                    break
            if j.primary_key is True and j.autoincrement is True:
                autoincrement_flag = True
        if primary_flag and autoincrement_flag and not repeat_flag:
            results.append(i)
    return results if results else None
