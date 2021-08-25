#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restplus import Resource, reqparse
from flask import g, jsonify

from controller.userController import userController
from utils import commons
from utils.response_code import RET


class UserOtherResource(Resource):

    # add
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', type=int, location='form', required=False, help='UserID参数类型不正确或缺失')
        parser.add_argument('UserName', type=str, location='form', required=False, help='UserName参数类型不正确或缺失')
        parser.add_argument('CreateTime', type=str, location='form', required=False, help='CreateTime参数类型不正确或缺失')
        parser.add_argument('IsDelete', type=int, location='form', required=False, help='IsDelete参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)

        res = userController.add(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # list query
    @classmethod
    def get(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', type=int, location='form', required=False, help='UserID参数类型不正确或缺失')
        parser.add_argument('UserName', type=str, location='form', required=False, help='UserName参数类型不正确或缺失')
        parser.add_argument('CreateTime', type=str, location='form', required=False, help='CreateTime参数类型不正确或缺失')
        parser.add_argument('IsDelete', type=int, location='form', required=False, help='IsDelete参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)

        res = userController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])
