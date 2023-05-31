#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:request_util.py
# author:Triblew
# datetime:2022/4/8 19:29
# software: PyCharm

"""
    this is function description
"""
import requests


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