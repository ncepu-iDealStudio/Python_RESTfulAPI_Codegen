#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    this is function description
"""

import requests
from loguru import logger


class RequestUtil:
    session = requests.session()

    @classmethod
    def send_request(cls, method, url, headers, data):
        method = str(method).lower()
        res = None

        if method == 'get':
            res = cls.session.request(method=method, url=url, headers=headers, params=data)
        elif method in ['put', 'post', 'delete']:
            res = cls.session.request(method=method, url=url, headers=headers, data=data)

        return res

    @classmethod
    def test_body(cls, caseInfo, env_dict):
        name = caseInfo.get("name")
        method = caseInfo['request']['method']
        headers = caseInfo['request'].get('headers')
        url = env_dict['base_url'] + caseInfo['request']['url']
        data = caseInfo['request'].get('params') if str(method).lower() == 'get' else caseInfo['request'].get('data')
        validates = caseInfo['validate']

        logger.info(f"{name}测试开始")
        logger.info(f"接口请求url为: {url}")
        logger.info(f"接口请求方式为: {method}")
        logger.info(f"接口请求头为: {headers}")
        logger.info(f"接口请求数据为: {data}")

        res = cls.send_request(method, url, headers, data)

        try:
            res_data = res.json()
        except Exception as e:
            logger.exception(f"返回的结果格式不正确。错误信息如下:\n{e}")
            raise Exception(f"返回的结果格式不正确。错误信息如下:\n{e}")

        # 断言内容
        for validate in validates:
            if validate['eq'][0] == 'status_code':
                logger.info(f"{validate['eq'][0]}预期结果为{validate['eq'][1]}")
                logger.info(f"实际结果为{res.__getattribute__(validate['eq'][0])}")
                assert res.__getattribute__(validate['eq'][0]) == validate['eq'][1]
                logger.info("断言成功")
            else:
                logger.info(f"{validate['eq'][0]}预期结果为{validate['eq'][1]}")
                logger.info(f"实际结果为{res_data.get(validate['eq'][0])}")
                assert res_data.get(validate['eq'][0]) == validate['eq'][1]
                logger.info("断言成功")

        logger.info(f"{name}测试通过")
        logger.info("\n")  # 分割不同用例
