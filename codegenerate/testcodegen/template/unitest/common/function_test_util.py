#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    this is function description
"""


import importlib
from loguru import logger
from manage import app

class FunctionTestUtil:

    @classmethod
    def test_body(cls, caseInfo):
        module_name = caseInfo['module_name']
        class_name = caseInfo['class_name']
        funtion_name = caseInfo['funtion_name']
        params = caseInfo.get('params')
        validates = caseInfo.get('validate')

        logger.info(f"方法service::{module_name}::{class_name}::{funtion_name}测试开始")
        logger.info(f"参数为{params}")

        module = importlib.import_module("service." + module_name)
        class_object = module.__getattribute__(class_name)
        with app.app_context():
            res = getattr(class_object, funtion_name)(**params)

            # 断言
            for validate in validates:
                logger.info(f"{validate['eq'][0]}预期结果为{validate['eq'][1]}")
                logger.info(f"实际结果为{res.get(validate['eq'][0])}")
                assert res.get(validate['eq'][0]) == validate['eq'][1]
                logger.info("断言成功")

        logger.info(f"方法service::{module_name}::{class_name}::{funtion_name}测试通过")
        logger.info("\n")  # 分割不同用例
