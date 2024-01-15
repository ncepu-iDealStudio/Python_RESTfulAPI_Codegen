#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify
from utils.response_code import RET


class ApiVersionResource(Resource):

    # get the interface of apiversion -- test
    def get(self):
        back_data = {
            'version': '1.0'
        }
        return jsonify(code=RET.OK, message='OK', data=back_data)    
