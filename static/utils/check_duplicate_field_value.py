#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:check_duplicate_field_value.py
# author:Chen Qinyu
# datetime:2022/5/25 16:34
# software: PyCharm

"""
    不可重复字段验证函数，且该字段为非加密字段
"""
from app import db
from functools import wraps
from .response_code import RET, error_map_EN


def check_duplicate_field_value(not_repeatable_list, model, **kwargs):
    """
    定义一个装饰器: 验证不可重复的字段，且该字段为非加密字段
    :param not_repeatable_list: List[Str] 字段不可重复
    :param model: 表
    :kwargs: 获取装饰器的传参(以下为示例参数)
    :other_column_list: List[Str] 其他自定义处理的相关字段列表

    eg.
    class AController:
        @classmethod
        @check_duplicate_field_value(['column1'], model=A)
        def add(cls):
            pass

        @classmethod
        @check_duplicate_field_value(['column1'], model=A, key='primary_key')
        def update(cls, primary_key):
            pass
    """

    def check_duplicate(func):
        """
        获取函数
        """

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            """
            获取函数传参
            """
            for field in not_repeatable_list:

                # 查询不可重复的字段，是否在数据库中已存在，存在则打回
                filter_list = [model.isDelete == 0]

                # 若接收到了该字段
                if field_value := func_kwargs.get(field):

                    # 如果是修改操作，则需要主键作为筛选条件
                    if key := kwargs.get('key'):
                        filter_list.append(getattr(model, key) != func_kwargs.get(key))

                    else:
                        filter_list.append(getattr(model, field) == field_value)

                    exist = db.session.query(model).filter(*filter_list).first()
                    if exist:
                        return {'code': RET.DATAEXIST, 'message': error_map_EN[RET.DATAEXIST], 'data': {'error': f'{field} already exists!'}}

            return func(*func_args, **func_kwargs)

        return wrapper

    return check_duplicate
