#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:not_repeatable.py
# author:Chen Qinyu
# datetime:2022/5/25 16:34
# software: PyCharm

"""
    不可重复字段验证函数
"""
from app import db
from functools import wraps

from . import commons
from .response_code import RET, error_map_EN
from .aes_encrypt_decrypt import AESEncryptDecrypt
from .rsa_encryption_decryption import RSAEncryptionDecryption


def verify_not_repeatable(not_repeatable_list, model, **kwargs):
    """
    定义一个装饰器: 验证不可重复的字段
    :param not_repeatable_list: List[Str] 字段不可重复
    :param model: 表
    :kwargs: 获取装饰器的传参(以下为示例参数)
    :aes_encrypt_list: List[Str] 不可重复且aes加密字段列表
    :rsa_encrypt_list: List[Str] 不可重复且rsa加密字段列表
    :other_column_list: List[Str] 其他自定义处理的相关字段列表

    eg.
    class AController:
        @classmethod
        @verify_not_repeatable(['column1'], model=A, rsa_encrypt_list=['column2'])
        def add(cls):
            pass

        @classmethod
        @verify_not_repeatable(['column1'], model=A, key='primary_key', aes_encrypt_list=['column2'])
        def update(cls, primary_key):
            pass
    """

    def verify_no_repeat(func):
        """
        获取函数
        """

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            """
            获取函数传参
            """
            # aes_encrypt_list = kwargs.get('aes_encrypt_list') if kwargs.get('aes_encrypt_list') else []
            # rsa_encrypt_list = kwargs.get('rsa_encrypt_list') if kwargs.get('rsa_encrypt_list') else []
            # for field in (not_repeatable_list + aes_encrypt_list + rsa_encrypt_list):
            #     # 查询不可重复的字段，是否在数据库中已存在，存在则打回
            #     filter_list = [model.isDelete == 0]
            #     # 若接收到了该字段
            #     if field_value := func_kwargs.get(field):
            #         # 如果是修改操作，则需要主键作为筛选条件
            #         if key := kwargs.get('key'):
            #             filter_list.append(getattr(model, key) != func_kwargs.get(key))
            #         # 且该字段为加密字段
            #         if field in aes_encrypt_list:
            #             filter_list.append(getattr(model, field) == AESEncryptDecrypt.encrypt(field_value))
            #         elif field in rsa_encrypt_list:
            #             field_info = db.session.query(getattr(model, field)).filter(*filter_list).all()
            #             results = commons.query_to_dict(field_info)
            #             lst = [RSAEncryptionDecryption.decrypt(res[field]) for res in results]
            #             if field_value in lst:
            #                 return {'code': RET.DATAEXIST, 'message': error_map_EN[RET.DATAEXIST], 'data': {'error': f'{field} already exists!'}}
            #         else:
            #             filter_list.append(getattr(model, field) == field_value)
            #
            #         exist = db.session.query(model).filter(*filter_list).first()
            #         if exist:
            #             return {'code': RET.DATAEXIST, 'message': error_map_EN[RET.DATAEXIST], 'data': {'error': f'{field} already exists!'}}
            pass
            return func(*func_args, **func_kwargs)

        return wrapper

    return verify_no_repeat
