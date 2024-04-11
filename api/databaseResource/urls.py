#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
from . import database_blueprint

from api.databaseResource.databaseResource import  DatabaseResource

api = Api(database_blueprint)

@database_blueprint.route('/database/conn_test',methods=['POST'],endpoint='conn_test')
def conn_test():
    return DatabaseResource.db_conn_test()

@database_blueprint.route('/database/get_database_names',methods=['GET'],endpoint='get_database_names')
def conn_test():
    return DatabaseResource.get_database_names()



