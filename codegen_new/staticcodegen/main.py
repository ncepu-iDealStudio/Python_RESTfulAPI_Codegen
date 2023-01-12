#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:createTableForTest.py
# author:Nathan
# datetime:2021/8/21 16:38
# software: PyCharm

"""
    静态资源层代码生成入口
"""

import os

from codegen_new.staticcodegen.codegenerator import CodeGenerator
from codegen_new.staticcodegen.template.filetemplate import FileTemplate
from utils.loggings import loggings


def main(settings, session_id, ip):
    """
    步骤：
        一、 按照当前项目的config/security.conf 文件 生成 static/config/security.conf
        二、 生成static/app 的setting.py文件
        三、 拷贝static 到 dist文件夹
    :return:
    """

    try:
        project_dir = settings.PROJECT_DIR

        # 第一步
        os.makedirs(os.path.join(project_dir, "config"), exist_ok=True)
        CodeGenerator.generate_develop_configuration_file(os.path.join(project_dir, "config", "develop_config.conf"),
                                                          settings, session_id, ip)
        CodeGenerator.generate_blank_configuration_file(os.path.join(project_dir, "config", "test_config.conf"),
                                                        settings, session_id, ip)
        CodeGenerator.generate_blank_configuration_file(os.path.join(project_dir, "config", "product_config.conf"),
                                                        settings, session_id, ip)

        # 第二步 app_setting
        app_setting_dir = os.path.join(project_dir, 'app')
        os.makedirs(app_setting_dir, exist_ok=True)
        with open(app_setting_dir + '/setting.py', 'w', encoding='utf8') as f:
            f.write(FileTemplate.app_setting)

        # 第三步 获取静态资源目录
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        source_dir = os.path.join(BASE_DIR, 'static')
        # 创建目标路径
        os.makedirs(project_dir, exist_ok=True)
        # 调用静态资源生成函数
        CodeGenerator.static_generate(project_dir, source_dir, session_id, ip)

        # 第四步 生成gunicorn.py
        project_name = settings.PROJECT_NAME
        CodeGenerator.gunicorn_generate(project_dir, project_name, session_id, ip)

    except Exception as e:
        loggings.exception(1, e, session_id, ip)
