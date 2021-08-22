#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file:start.py
# author:Nathan
# datetime:2021/8/20 21:35
# software: PyCharm
"""
    this is function description
"""

from sqlacodegen.controllercodegen import controllerGenerate
from sqlacodegen.modelcodegen import modelGenerate
from sqlacodegen.resourcecodegen import resourceGenerate
from sqlacodegen.staticcodegen import staticGenerate


if __name__ == '__main__':
    """
        步骤：
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Resource层代码
            四、 打包静态文件
            五、 目标项目启动
            六、 目标项目接口测试
    """

    # 第一步
    print("开始构建Model层代码, 请稍等...")
    modelGenerate()
    print("构建Model层代码完成")

    # 第二步
    print("开始构建Controller层代码, 请稍等...")
    controllerGenerate()
    print("构建Controller层代码完成")

    # 第三步
    print("开始构建Resource层代码, 请稍等...")
    resourceGenerate()
    print("构建Resource层代码完成")

    # 第四步
    print("开始打包静态文件, 请稍等...")
    staticGenerate()
    print("打包静态文件完成")

    print("生成完成")
