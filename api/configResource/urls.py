#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
from . import config_blueprint

from api.configResource.configResource import  ConfigResource

api = Api(config_blueprint)

@config_blueprint.route('/config/write',methods=['POST'],endpoint='conn_test')
def write_user_config():
    ConfigResource.write_user_config()






