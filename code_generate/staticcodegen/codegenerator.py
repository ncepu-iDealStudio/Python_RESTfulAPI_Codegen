#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegenerator.py
# author:Nathan
# datetime:2021/8/27 11:45
# software: PyCharm

"""
    this is function description
"""

import os
import shutil
from configparser import ConfigParser
from .template import filetemplate
from utils.loggings import loggings


class CodeGenerator(object):
    SECURITY_CONFIG_DIR = "config/security.conf"
    SECURITY_CONFIG = ConfigParser()
    SECURITY_CONFIG.read(SECURITY_CONFIG_DIR, encoding='utf-8')

    @classmethod
    def generate_develop_configuration_file(cls, configuration_file_path, settings, session_id, ip):
        """
            :param configuration_file_path: 配置文件存储路径
            :param settings: 用户配置
            :param session_id: 用户ID
            :param ip: 用户IP地址
            :return: None
        """
        try:
            dialect = settings.DIALECT
            driver = settings.DRIVER
            username = settings.USERNAME
            password = settings.PASSWORD
            host = settings.HOST
            port = settings.PORT
            database = settings.DATABASE

            target_config = ConfigParser()

            # write configueration about databse
            target_config.add_section("DATABASE")
            target_config.set("DATABASE", "DIALECT", dialect)
            target_config.set("DATABASE", "DRIVER", driver)
            target_config.set("DATABASE", "USERNAME", username)
            target_config.set("DATABASE", "PASSWORD", password)
            target_config.set("DATABASE", "HOST", host)
            target_config.set("DATABASE", "PORT", port)
            target_config.set("DATABASE", "DATABASE", database)
            target_config.set("DATABASE", "SQLALCHEMY_TRACK_MODIFICATIONS", "True")
            target_config.set("DATABASE", "SQLALCHEMY_POOL_SIZE", '50')
            target_config.set("DATABASE", "SQLALCHEMY_MAX_OVERFLOW", '-1')

            for section in cls.SECURITY_CONFIG.sections():
                target_config.add_section(section)
                for option_key, option_value in cls.SECURITY_CONFIG.items(section):
                    target_config.set(section, option_key, option_value)

            with open(configuration_file_path, 'w', encoding="utf-8") as f:
                target_config.write(f)

        except Exception as e:
            loggings.exception(1, e, session_id, ip)

    @classmethod
    def generate_blank_configuration_file(cls, configuration_file_path, settings, session_id, ip):
        """
            :param configuration_file_path: 配置文件存储路径
            :param settings: 用户配置
            :param session_id: 用户ID
            :param ip: 用户IP地址
            :return: None
        """
        try:
            dialect = settings.DIALECT
            driver = settings.DRIVER

            target_config = ConfigParser()

            # write configueration about databse
            target_config.add_section("DATABASE")
            target_config.set("DATABASE", "DIALECT", dialect)
            target_config.set("DATABASE", "DRIVER", driver)
            target_config.set("DATABASE", "USERNAME", "")
            target_config.set("DATABASE", "PASSWORD", "")
            target_config.set("DATABASE", "HOST", "")
            target_config.set("DATABASE", "PORT", "")
            target_config.set("DATABASE", "DATABASE", "")
            target_config.set("DATABASE", "SQLALCHEMY_TRACK_MODIFICATIONS", "True")
            target_config.set("DATABASE", "SQLALCHEMY_POOL_SIZE", '50')
            target_config.set("DATABASE", "SQLALCHEMY_MAX_OVERFLOW", '-1')

            # write configueration about BASIC
            target_config.add_section("BASIC")
            target_config.set("BASIC", "token_expires", "3600")

            for section in cls.SECURITY_CONFIG.sections():
                if section != 'BASIC':
                    target_config.add_section(section)
                    for option_key, option_value in cls.SECURITY_CONFIG.items(section):
                        target_config.set(section, option_key, "")

            with open(configuration_file_path, 'w', encoding="utf-8") as f:
                target_config.write(f)

        except Exception as e:
            loggings.exception(1, e, session_id, ip)

    @classmethod
    def static_generate(cls, target_dir, source_dir, session_id, ip):
        """
        1 copy the static resource to target project directory;
        2 you can put these static resource  into "static" directory,such as "dockerfile" and some
         common tools(or function) that you will use in your target project;
        3 some resource we need has already copied into default static directory;
        :param target_dir: Target path of the file
        :param source_dir: Source path of the file
        :param session_id: The ID of User
        :param ip: The IP Host of User
        :return: None
        """

        try:
            # 判断目标路径状态
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # 拷贝
            if os.path.exists(source_dir):
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        # 源文件路径
                        src_file = os.path.join(root, file)
                        # 目标文件路径
                        target_file = target_dir + root.replace(source_dir, '')
                        if not os.path.exists(target_file):
                            os.makedirs(target_file)
                        # 拷贝
                        shutil.copy(src_file, target_file)
                        loggings.info(1, "The file '{}' has been copied to '{}'".format(src_file, target_file),
                                      session_id, ip)

        except Exception as e:
            loggings.exception(1, e, session_id, ip)

    @classmethod
    def gunicorn_generate(cls, target_dir, project_name, session_id, ip):
        """
            :param target_dir: 项目文件存储路径
            :param project_name: 项目名称
            :param session_id: 用户ID
            :param ip: 用户IP地址
            :return: None
        """
        try:
            with open(os.path.join(target_dir, 'gunicorn.py'), 'w', encoding='utf8') as f:
                f.write(filetemplate.gunicorn.format(project_name=project_name))
        except Exception as e:
            loggings.exception(1, e, session_id, ip)
