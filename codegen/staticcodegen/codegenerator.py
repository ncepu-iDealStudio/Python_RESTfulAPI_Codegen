#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegenerator.py
# author:Nathan
# datetime:2021/8/27 11:45
# software: PyCharm

"""
    this is function description
"""

from configparser import ConfigParser

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
