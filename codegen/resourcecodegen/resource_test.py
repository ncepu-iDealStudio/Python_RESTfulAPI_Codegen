#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restplus import Resource, reqparse
from flask import g, jsonify

from controller.userController import userController
from utils import commons
from utils.response_code import RET


class UserResource(Resource):

    # query with primary_key
    @classmethod
    def get(cls, AutoID):
        kwargs = {}

        if not AutoID:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs['AutoID'] = AutoID

        res = UserController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # delete
    @classmethod
    def delete(cls, AutoID):
        kwargs = {}

        if not AutoID:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs['AutoID'] = AutoID

        res = UserController.delete(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])

    # put
    @classmethod
    def put(cls, AutoID):
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', type=int, location='form', required=False, help='UserID参数类型不正确或缺失')
        parser.add_argument('UserName', type=str, location='form', required=False, help='UserName参数类型不正确或缺失')
        parser.add_argument('CreateTime', type=str, location='form', required=False, help='CreateTime参数类型不正确或缺失')
        parser.add_argument('IsDelete', type=int, location='form', required=False, help='IsDelete参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(*kwargs)

        if not AutoID:
            return jsonify(code=RET.NODATA, message='primary_key missed', error='primary_key missed')
        kwargs['AutoID'] = AutoID

        res = UserController.put(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'])
        else:
            return jsonify(code=res['code'], message=res['message'], error=res['error'])
