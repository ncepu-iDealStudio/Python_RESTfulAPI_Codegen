#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:copyfile.py
# author:Nathan
# datetime:2021/8/27 11:28
# software: PyCharm

"""
    拷贝目标项目所需要的静态配置等文件
"""

import os
import shutil
from utils.loggings import loggings


def copy_static(target_dir, source_dir):
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
