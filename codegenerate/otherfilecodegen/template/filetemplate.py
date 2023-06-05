#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:PigKinght
# datetime:2021/8/26 10:55
# software: PyCharm

"""
    the template file define.
"""


class FileTemplate():
    """
    app_init_: template for app/__init__.py
    app_setting_: template for app/__setting__.py
    """

    app_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

\"\"\"
   应用初始化文件模板
\"\"\"

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .setting import Settings
from models import db

# 工厂模式创建app应用对象
def create_app(run_mode):
    \"\"\"
    创建flask的应用对象
    :param run_mode: string 配置模式的名字  （"develop", "product", "test"）
    :return:
    \"\"\"
    
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    app.config.from_object(Settings.get_setting(run_mode))

    # 使用app初始化db
    db.init_app(app)

    # 利用Flask_session将数据保存的session中
    Session(app)

    # 调用resource层中定义的方法，初始化所有路由(注册)蓝图
    from api_{api_version} import init_router
    init_router(app)
    
    return app
"""

    manage = """#!/usr/bin/python3
# -*- coding: utf-8 -*-

\"\"\"
   入口程序
\"\"\"

from app import create_app
from flask_script import Manager, Server
from flask import request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.response_code import RET

# 创建flask的app对象
app = create_app("develop")

# 通过Flask-Script的Manager,Server接管Flask运行
manager = Manager(app)

# 开启Debug模式
manager.add_command("runserver", Server(use_debugger=True))


# 创建全站拦截器,每个请求之前做处理
@app.before_request
def user_validation():
    print(request.endpoint)  # 方便跟踪调试
    
    if not request.endpoint: # 如果请求点为空
        return jsonify(code=RET.URLNOTFOUND, message="url not found", error="url not found")
        
@app.before_request
def user_require_token():
    # 不需要token验证的请求点列表
    permission = {permission}

    # 如果不是请求上述列表中的接口，需要验证token
    if request.endpoint not in permission:
        # 在请求头上拿到token
        token = request.headers.get("Token")
        if not all([token]):
            return jsonify(code=RET.PARAMERR, message="缺少参数Token或请求非法")

        # 校验token格式正确与过期时间
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except Exception as e:
            app.logger.error(e)
            # 单平台用户登录失效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期')


# 创建全站拦截器，每个请求之后根据请求方法统一设置返回头
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://api.youwebsite.com':
            response.headers["Access-Control-Allow-Origin"] = 'http://api.youwebsite.com'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token,Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response


if __name__ == "__main__":
    manager.run()

"""