#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:md5_encrypt_decrypt.py
# author:jackiex
# datetime:2022/7/19 16:24
# software: PyCharm

"""
    this is function  description
"""

import hashlib
import base64
from configparser import ConfigParser

# 设置配置文件的位置
CONFIG_DIR = "config/develop_config.conf"
CONFIG = ConfigParser()
CONFIG.read(CONFIG_DIR, encoding='utf-8')


class UserDefineEncryptionDecryption(object):
    """
        用户自定义加密方法，用于存储需要加密的字段值到数据库
    """

    salt_key = CONFIG['BASIC']['secret_key']

    # md5+盐加密
    @classmethod
    def md5_salt_encrypt(cls, string, salt_key):
        """
        parameter:string:明文(需要加密的)；
        parameter:salt_key:盐；
        return value：加密后的密文
        """
        str_temp = str(string).join(salt_key)  # MD5加盐字符串处理

        md_sale = hashlib.md5(str_temp.encode())  # MD5加盐加密

        return md_sale.hexdigest()

    # base64简单加密
    @classmethod
    def base64_encrypt(cls, string):
        """
        parameter:string:明文(需要加密的)；
        return value：加密后的密文
        """
        string_bytes = string.encode()  # 把字符串转为字节类型
        str_base64 = base64.b64encode(string_bytes)  # base64 编码

        return str_base64

    # base64字符串解密
    @classmethod
    def base64_decrypt(cls, string):
        return base64.b64decode(string)

    # base64字符串+盐加密
    @classmethod
    def base64_salt_encrypt(cls, string, salt_key):
        string_bytes = (str(string).join(salt_key)).encode()

        str_base64 = base64.b64encode(string_bytes)  # base64 编码

        return str_base64
