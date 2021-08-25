#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

from . import urls

user_blueprint = Blueprint('user', __name__)
