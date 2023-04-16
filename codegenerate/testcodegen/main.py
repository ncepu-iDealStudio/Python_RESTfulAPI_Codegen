#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:50
# Author:yuanronghao
# @File:main.py.py
# @Software:PyCharm


import os
from shutil import copyfile

from codegenerate.testcodegen.codegenerator import CodeGenerator
from codegenerate.testcodegen.core.filetemplate import FileTemplate
from utils.loggings import loggings


def generate_test_layer(table_dict, settings, session_id, ip):
    """
    Generate resource layer code
    :return: None
    """
    project_dir = settings.PROJECT_DIR
    target_dir = settings.TARGET_DIR

    try:
        if not list(table_dict.keys()):
            return

        # Get target directory
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(project_dir, exist_ok=True)

        test_dir = os.path.join(project_dir, 'test')
        os.makedirs(test_dir, exist_ok=True)

        report_dir = os.path.join(test_dir, 'report')
        os.makedirs(report_dir, exist_ok=True)

        temp_dir = os.path.join(test_dir, 'temps')
        os.makedirs(temp_dir, exist_ok=True)

        # copy template dir to test dir
        copy_dir(os.path.join(os.getcwd(), "codegenerate\\testcodegen\\template"), test_dir)

        test_env = os.path.join(test_dir, '.env')
        with open(test_env, 'w', encoding='utf8') as f:
            f.write(FileTemplate.env.format(project_name=project_dir.replace('\\', '/').split('/')[-1]))

        generator = CodeGenerator()
        generator.test_generator(test_dir, table_dict, session_id, ip)

    except Exception as e:
        loggings.error(1, str(e), session_id, ip)


def copy_dir(src_dir, dst_dir):
    """
    复制src_dir目录下的所有内容到dst_dir目录
    :param src_dir: 源文件目录
    :param dst_dir: 目标目录
    :return:
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if os.path.exists(src_dir):
        for file in os.listdir(src_dir):
            file_path = os.path.join(src_dir, file)
            dst_path = os.path.join(dst_dir, file)
            if os.path.isfile(os.path.join(src_dir, file)):
                copyfile(file_path, dst_path)
            else:
                copy_dir(file_path, dst_path)
