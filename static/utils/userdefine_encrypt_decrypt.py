#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:md5_encrypt_decrypt.py
# author:jackiex
# datetime:2022/7/19 16:24
# software: PyCharm

'''
    this is function  description 
'''

import hashlib
from configparser import ConfigParser

CONFIG_DIR = "config/develop_config.conf"
CONFIG = ConfigParser()
CONFIG.read(CONFIG_DIR, encoding='utf-8')

class UserDefineEncryptionDecryption(object):
    """
        用户自定义加密方法，用于存储需要加密的字段值到数据库
    """

    salt_key = CONFIG['BASIC']['secret_key']

    # RSA加密
    @classmethod
    def encrypt(cls, string,salt_key):

        str_temp = str(string).join(salt_key)

        md_sale = hashlib.md5(str_temp.encode())  # MD5加盐加密

        return md_sale.hexdigest()
