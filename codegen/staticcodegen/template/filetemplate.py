#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:Nathan
# datetime:2021/8/27 13:19
# software: PyCharm

"""
    this is function description
"""


class FileTemplate(object):
    app_setting = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
  应用的配置加载项
\"\"\"

import os
from configparser import ConfigParser
from urllib import parse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件和数据文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')


class Settings(object):
    CONFIG = ConfigParser()

    @classmethod
    def get_setting(cls, runMode):
        cls.CONFIG.read(os.path.join(CONFIG_DIR, runMode + '_config.conf'), encoding='utf-8')

        # 秘钥
        cls.SECRET_KEY = cls.CONFIG['AES']['secret_key']
        cls.PUBLIC_KEY = cls.CONFIG['RSA']['public_key']
        cls.PRIVATE_KEY = cls.CONFIG['RSA']['private_key']

        # debug模式
        # DEBUG = DEVELOP_CONFIG.getboolean('STATIC_CONFIG', 'DEBUG')

        # 数据库配置
        cls.DIALECT = cls.CONFIG['DATABASE']['dialect']
        cls.DRIVER = cls.CONFIG['DATABASE']['driver']
        cls.USERNAME = cls.CONFIG['DATABASE']['username']
        cls.PASSWORD = cls.CONFIG['DATABASE']['password']
        cls.HOST = cls.CONFIG['DATABASE']['host']
        cls.PORT = cls.CONFIG['DATABASE']['port']
        cls.DATABASE = cls.CONFIG['DATABASE']['database']

        cls.SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            cls.DIALECT, cls.DRIVER, cls.USERNAME, parse.quote_plus(cls.PASSWORD), cls.HOST, cls.PORT, cls.DATABASE)

        cls.SQLALCHEMY_TRACK_MODIFICATIONS = cls.CONFIG.getboolean('DATABASE', 'sqlalchemy_track_modifications')

        # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
        cls.SQLALCHEMY_POOL_SIZE = int(cls.CONFIG['DATABASE']['sqlalchemy_pool_size'])

        # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
        cls.SQLALCHEMY_MAX_OVERFLOW = int(cls.CONFIG['DATABASE']['sqlalchemy_max_overflow'])

        # token的有效期,单位：秒
        cls.TOKEN_EXPIRES = int(cls.CONFIG['BASIC']['token_expires'])

        return cls

"""


gunicorn = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
    gunicorn启动文件
\"\"\"

import os
import sys


def start():
    cmd = 'source /deploy/app/venv/bin/activate;' \\
          'cd /deploy/your project;' \\
          'gunicorn -c deploy/gunicorn.conf manage:app -D'
    os.system(cmd)


def stop():
    cmd = "ps -ef | grep '{project_name}/bin/gunicorn' | grep -v grep | awk '{{print $2}}' | xargs kill -9"
    os.system(cmd)


def restart():
    stop()
    start()


if sys.argv[1] == 'start':
    start()
elif sys.argv[1] == 'restart':
    restart()
elif sys.argv[1] == 'stop':
    stop()
else:
    print('params error!')
"""
