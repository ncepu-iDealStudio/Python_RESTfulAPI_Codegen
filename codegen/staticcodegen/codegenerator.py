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

from config.setting import Settings
from utils.loggings import loggings


class CodeGenerator(object):
    SECURITY_CONFIG_DIR = "config/security.conf"
    SECURITY_CONFIG = ConfigParser()
    SECURITY_CONFIG.read(SECURITY_CONFIG_DIR, encoding='utf-8')

    @classmethod
    def generate_configuration_file(cls, configuration_file_path):
        """
        :param configuration_file_path: The path where the configuration file is stored
        :return: None
        """
        try:
            target_config = ConfigParser()

            # write configueration about databse
            target_config.add_section("DATABASE")
            target_config.set("DATABASE", "DIALECT", Settings.DIALECT)
            target_config.set("DATABASE", "DRIVER", Settings.DRIVER)
            target_config.set("DATABASE", "USERNAME", Settings.USERNAME)
            target_config.set("DATABASE", "PASSWORD", Settings.PASSWORD)
            target_config.set("DATABASE", "HOST", Settings.HOST)
            target_config.set("DATABASE", "PORT", Settings.PORT)
            target_config.set("DATABASE", "DATABASE", Settings.DATABASE)
            target_config.set("DATABASE", "SQLALCHEMY_TRACK_MODIFICATIONS", Settings.SQLALCHEMY_TRACK_MODIFICATIONS)
            target_config.set("DATABASE", "SQLALCHEMY_POOL_SIZE", Settings.SQLALCHEMY_POOL_SIZE)
            target_config.set("DATABASE", "SQLALCHEMY_MAX_OVERFLOW", Settings.SQLALCHEMY_MAX_OVERFLOW)

            for section in cls.SECURITY_CONFIG.sections():
                # 'RSA_TABLE_COLUMN' section is not required
                if section == 'RSA_TABLE_COLUMN':
                    continue
                target_config.add_section(section)
                for option_key, option_value in cls.SECURITY_CONFIG.items(section):
                    target_config.set(section, option_key, option_value)

            with open(configuration_file_path, 'w', encoding="utf-8") as f:
                target_config.write(f)
        except Exception as e:
            loggings.exception(1, e)

    @classmethod
    def static_generate(cls, target_dir, source_dir):
        """
        1 copy the static resource to target project directory;
        2 you can put these static resource  into "static" directory,such as "dockerfile" and some
         common tools(or function) that you will use in your target project;
        3 some resource we need has already copied into default static directory;
        :param target_dir: Target path of the file
        :param source_dir: Source path of the file
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
                        loggings.info(1, "The file '{}' has been copied to '{}'".format(src_file, target_file))
        except Exception as e:
            loggings.exception(1, e)
