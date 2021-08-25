#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import user_blueprint
from api_1.userResource.userResource import UserResource
from api_1.userResource.userOtherResource import UserOtherResource

api = APi(user_blueprint)

api.add_resource(UserResource, '/<int:AutoID>', endpoint='user')

api.add_resource(UserOtherResource, '', endpoint='user_list')
