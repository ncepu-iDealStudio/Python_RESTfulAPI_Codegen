#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:task.py
# author:Triblew
# datetime:2022/4/8 21:31
# software: PyCharm

"""
    this is function description
"""

from locust import HttpUser, User

from test.performance_test.task.login_task.login_task import LoginTask
from test.performance_test.task.search_task.search_task import SearchTask


class HTTPUser(HttpUser):
    # 任务集
    tasks = [LoginTask, SearchTask]
    min_wait = 1000
    max_wait = 2000


class DBUser(User):
    abstract = True
