#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:Nathan
# datetime:2021/8/20 21:35
# software: PyCharm

"""
    this is function description
"""

import codegen.servicecodegen.main
import codegen.staticcodegen.main
import codegen.controllercodegen.main
import codegen.resourcecodegen.main
import codegen.modelcodegen.main
import codegen.testcodegen.main

from utils.checkConfig import check_config
from utils.loggings import loggings


def start():
    """
        步骤：
            零、 配置文件参数检查
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Service层代码
            四、 生成Resource层代码
            五、 打包静态文件
    """

    # 第零步
    # if not check_config():
    #     loggings.error(1, "Incorrect Configuration File")
    #     return

    # 第一步
    loggings.info(1, "Start to build the Model layer code, please wait...")
    codegen.modelcodegen.main.main()
    loggings.info(1, "Model layer code build completed")

    # 第二步
    loggings.info(1, "Start to build the Controller layer code, please wait...")
    codegen.controllercodegen.main.main()
    loggings.info(1, "Controller layer code build completed")

    # 第三步
    loggings.info(1, "Start to build the Service layer code, please wait...")
    codegen.servicecodegen.main.main()
    loggings.info(1, "Service layer code build completed")

    # 第四步
    loggings.info(1, "Start to build the Resource layer code, please wait...")
    codegen.resourcecodegen.main.main()
    loggings.info(1, "Resource layer code build completed")

    # 第五步
    loggings.info(1, "Start packing static files, please wait...")
    codegen.staticcodegen.main.main()
    loggings.info(1, "Static resource packaging is complete")

    loggings.info(1, "Api project code generation completed")

    # 第六步
    loggings.info(1, "Start to build the Test layer code, please wait...")
    codegen.testcodegen.main.main()
    loggings.info(1, "Test layer code build completed")
