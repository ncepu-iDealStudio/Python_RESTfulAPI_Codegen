#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
from . import user_blueprint
from api.userResource.userResource import  UserResource

api = Api(user_blueprint)

@user_blueprint.route('/user/session',methods=['GET'],endpoint='user')
def get_user_session():
    return UserResource.get_user_session()
