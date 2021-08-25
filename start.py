#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start.py
# author:Nathan
# datetime:2021/8/20 21:35
# software: PyCharm

"""
    this is function description
"""

from codegen.controllercodegen import controllerGenerate
from codegen.modelcodegen.main import modelGenerate
from codegen.resourcecodegen import resourceGenerate
from codegen.staticcodegen import staticGenerate
from utils.checkConfig import check_config
from utils.loggings import loggings

if __name__ == '__main__':
    """
        步骤：
            零、 配置文件参数检查
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Resource层代码
            四、 打包静态文件
            五、 目标项目启动
            六、 目标项目接口测试
    """
    # 第零步
    if check_config():
        # 第一步
        loggings.info(1, "开始构建Model层代码, 请稍等...")
        modelGenerate()
        loggings.info(1, "构建Model层代码完成")

        # 第二步
        loggings.info(1, "开始构建Controller层代码, 请稍等...")
        controllerGenerate()
        loggings.info(1, "构建Controller层代码完成")

        # 第三步
        loggings.info(1, "开始构建Resource层代码, 请稍等...")
        resourceGenerate()
        loggings.info(1, "构建Resource层代码完成")

        # 第四步
        loggings.info(1, "开始打包静态文件, 请稍等...")
        staticGenerate()
        loggings.info(1, "打包静态文件完成")

        loggings.info(1, "生成完成")
    else:
        loggings.error(1, "配置文件有误")