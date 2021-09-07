#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start.py
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

from codegen.modelcodegen.main import modelGenerate
from utils.checkConfig import check_config
from utils.loggings import loggings

if __name__ == '__main__':
    """
        步骤：
            零、 配置文件参数检查
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Service层代码
            四、 生成Resource层代码
            五、 打包静态文件
            六、 目标项目启动
            七、 目标项目接口测试
    """
    # 第零步
    if check_config():
        # 第一步
        loggings.info(1, "Start to build the Model layer code, please wait...")
        # modelGenerate()
        loggings.info(1, "Model layer code build completed")

        # 第二步
        loggings.info(1, "Start to build the Controller layer code, please wait...")
        # codegen.controllercodegen.main.main()
        loggings.info(1, "Controller layer code build completed")

        # 第三步
        loggings.info(1, "Start to build the Service layer code, please wait...")
        # codegen.servicecodegen.main.main()
        loggings.info(1, "Service layer code build completed")

        # 第四步
        loggings.info(1, "Start to build the Resource layer code, please wait...")
        codegen.resourcecodegen.main.main()
        loggings.info(1, "Resource layer code build completed")

        # 第五步
        loggings.info(1, "Start packing static files, please wait...")
        # codegen.staticcodegen.main.main()
        loggings.info(1, "Static resource packaging is complete")

        loggings.info(1, "Api project code generation completed")

    else:
        loggings.error(1, "Incorrect Configuration File")
