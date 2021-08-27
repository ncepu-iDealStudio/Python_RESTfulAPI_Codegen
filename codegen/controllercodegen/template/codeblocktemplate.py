#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codeblocktemplate.py
# author:Itsuka
# datetime:2021/8/26 10:32
# software: PyCharm

"""
    provide code block template here
"""


class CodeBlockTemplate(object):

    imports = '''
from app import db
from models.{model_name} import {parent_model}
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.rsa_encryption_decryption import RSAEncryptionDecryption
from utils.loggings import loggings'''

    add_column_init = '''{column}=kwargs.get('{column}'),
                '''

    rsa_add = '''{column}=RSAEncryptionDecryption.encrypt(kwargs.get('{column}')),
                '''

    get_filter_num = '''if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                '''

    get_filter_str = '''if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                '''

    rsa_get_filter_num = '''if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
                '''

    rsa_get_filter_str = '''if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == RSAEncryptionDecryption.encrypt(kwargs.get('{column}')))
                '''

    rsa_update = '''if kwargs.get('{column}'):
                kwargs['{column}'] = RSAEncryptionDecryption.encrypt(kwargs['{column}'])
            '''
