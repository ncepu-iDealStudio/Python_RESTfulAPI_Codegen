#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    :2020/11/27 16:10
# @Author  :Jackiex
# @Software:PyCharm

"""
   入口程序
"""
# import module your need


from app import create_app
from flask_script import Manager
from flask import request, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.response_code import RET

# 创建flask的app对象
app = create_app("develop")

manager = Manager(app)


# 创建全站拦截器,每个请求之前做处理
@app.before_request
def user_require_token():
    print(request.endpoint)

    # 需要token验证的get请求点列表；
    get_not_permission = []

    if request.method in ['PUT', 'DELETE', 'POST'] or request.endpoint in get_not_permission:
        pass

    # 不需要token验证的请求点列表
    permission = ["experimentAndStudent.getNumber", "experimentAndStudent.getStudentinfo", "techTag.TechTag",
                  "course.single_course", "common.weixinbind","common.weixinLogin",'common.file_stream_download',
                  "teacher.teacher_studycontentlist", "course.course_list", "apiversion.apiversion",
                  "platform_user.platform_users_login", "experiment.experimentQuery",
                  "experiment.getExperiment",
                  "student.studentLogin", "student.student_register", "rotationPic.rotationPicInfo",
                  'studycontent.studycontentInfo_querylist', "experimentQandA.getreply",
                  "experimentQandA.experimentQandAQuery",
                  "experimentQandA.getExperimentQandA", "student.project_studentaddinfo",
                  "student.doc", "student.specs", "restplus_doc.static", "api_doc_blueprint.doc",
                  "api_doc_blueprint.specs",
                  "student.doc", "student.specs", "restplus_doc.static", "api_doc_blueprint.doc",
                  "api_doc_blueprint.specs", "common.verifycode", "techTag.TechTaglist",
                  "experimentType.experimentTypes", "experimentType.experimentType", "student.student_logout",
                  "experimentAndStudent.ProjectSelected", "teacher.teacher_login", "platform_user.sys_users_login",
                  "project.get_project", "project.get_projects", "classInfoAdmin.classInfo_list",
                  "college.college_list",
                  "rotationPicInfoAdmin.rotationPicInfo_list",
                  "experimentTeachBatch.getexperimentTeachBatch", "experimentTeachBatch.getexperimentTeachBatchs"
                  ]

    # 如果不是请求上述列表中的接口，需要验证token
    if request.endpoint not in permission:
        # 在请求头上拿到token
        token = request.headers.get("Token")
        if not all([token]):
            return jsonify(code=RET.PARAMERR, message="缺少参数Token或请求非法")

        # 校验token格式正确与过期时间（用户未点击退出）
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except Exception as e:
            app.logger.error(e)
            # 单平台用户登录失效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期')

        # 处理多平台登录的问题
        from controller.userTokenController import UserTokenController
        kwargs = {
            "UserID": data["id"],
            # "Usertype": data['user_type']
        }
        try:
            sql_token = UserTokenController.get_token(**kwargs).first().Token

        except Exception as e:
            # 校验token是否有效，用户点击退出后该token无效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期(已退出)', error=str(e))

        if token != sql_token:
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期(多平台)')

        # 将用户信息保存到g对象
        result_dict = UserTokenController.get_user_by_token(sql_token)
        if result_dict['code'] == '2000':
            g.user = result_dict['data']
        else:
            return jsonify(code=result_dict['code'], message=result_dict['message'])


# 创建全站拦截器，每个请求之后根据请求方法统一设置返回头
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://experiment.ncepu.edu.cn':
            response.headers["Access-Control-Allow-Origin"] = 'http://experiment.ncepu.edu.cn'
        # if request.headers.get('Origin') and request.headers['Origin'] == 'http://super.paper.ncepu.edu.cn':
        #     response.headers["Access-Control-Allow-Origin"] = 'http://super.paper.ncepu.edu.cn'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response


if __name__ == "__main__":
    manager.run()
