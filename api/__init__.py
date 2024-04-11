#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .databaseResource import database_blueprint

def init_router(app):
    from api.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api")

def init_router(app):
    from api.databaseResource import database_blueprint
    app.register_blueprint(database_blueprint, url_prefix="/api")
    
