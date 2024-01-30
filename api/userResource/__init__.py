#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

user_blueprint = Blueprint("user", __name__)

from . import urls
