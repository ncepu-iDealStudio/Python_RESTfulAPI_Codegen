#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:userResource.py
# author:jackiex
# datetime:2024/1/15 17:00
# software: PyCharm

'''
    this is function  description 
'''
from datetime import time

from flask import jsonify, session
from flask_restful import Resource

from utils.response_code import RET


class UserResource(Resource):
    def __init__(self):
        pass

    @classmethod
    def get_user_session(cls):
        session['id'] = int(round(time.time() * 1000))
        return jsonify(code=RET.OK, message="成功", data=session['id'])



