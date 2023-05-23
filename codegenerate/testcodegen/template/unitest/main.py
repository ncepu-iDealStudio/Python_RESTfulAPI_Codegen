#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    this is function description
"""

import os

import pytest

if __name__ == '__main__':
    # 执行测试脚本
    pytest.main()

    # 生成测试报告
    # 需要在本地安装allure，并且设置环境变量，否则这个命令将会报错
    res = os.system("allure generate ./temps -o ./reports --clean")
    if res != 0:
        raise ModuleNotFoundError(
            "需要为本地安装allure并设置环境变量,否则无法生成测试报告。参考allure仓库地址https://github.com/allure-framework/allure2/releases")
