#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:login_task.py
# author:Triblew
# datetime:2022/4/8 19:18
# software: PyCharm

"""
    this is function description
"""
import os

from locust import TaskSet, task
from test.performance_test.utils.read_yaml import read_yaml


# 任务类
class LoginTask(TaskSet):

    @task
    def login_task(self):
        case_info = read_yaml(os.path.join(os.path.dirname(__file__), "data.yaml"))
        name = case_info['request'].get('name')
        method = case_info['request'].get('method')
        headers = case_info['request'].get('headers')
        url = case_info['request'].get('url')
        data = case_info['request'].get('data')
        validates = case_info['validate']

        with self.client.request(method=method, url=url, json=data, headers=headers, name=name,
                                 catch_response=True) as response:
            for validate in validates:
                if validate['eq'][0] == 'status_code':
                    if response.__getattribute__(validate['eq'][0]) != validate['eq'][1]:
                        response.failure("Can not login!")
                        break
                else:
                    if response.json().get(validate['eq'][0]) != validate['eq'][1]:
                        response.failure("Can not login!")
                        break
                response.success()
