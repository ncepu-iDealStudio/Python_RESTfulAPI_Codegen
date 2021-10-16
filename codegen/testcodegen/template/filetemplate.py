#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:52
# Author:yuanronghao
# @File:filetemplate.py
# @Software:PyCharm

class FileTemplate(object):
    """
    init_: template for Test_Controller/init.py,Test_Resource/init.py,
    test_init_:template for test/init.py
    pytest_ini：template for test/pytest.ini
    Test_xController/init.py, Test_xResource/init.py
    controller_datas_:template for Test_xController/datas.py
    resource_datas_:template for Test_xResource/datas.py
    test_controller_: template for Test_xController/test_xController.py
    test_resource_: template for Test_xResource/test_xResource.py

    """

    init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
    """

    test_init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app import create_app

app = create_app("develop")
app.app_context().push()
"""

    pytest_ini = """
[pytest]
markers =
    resource: marks tests as resource
    controller: marks tests as controller
    service: marks tests as service

log_level = INFO
log_cli_level = INFO
log_format ="%(asctime)s %(levelname)s %(message)s"
log_cli_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %H:%M:%S
log_cli_date_format = %Y%M%D %H:%M:%S
log_file = ./logs/logs.log
log_file_format ="""

    test_start = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import webbrowser

# run all test
def start_test():
    # html report path
    dir_path = os.path.split(os.path.realpath(__file__))[0]
    html_report = r'{}\\report\\test_report.html'.format(dir_path)

    pytest.main(['-s', '-v', '--capture=sys', "--html={}".format(html_report)])


app = Flask(__name__, template_folder="./report", static_folder="./report/assets")
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("test_report.html")


if __name__ == '__main__':
    start_test()
    webbrowser.open('http://127.0.0.1:8001')
    app.run(port=8001)"""

    controller_datas = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
# add test_datas here:
# example:
# add_datas = [
#     {
#         'UserID': 123456789,
#         'UserName':xxxxxx,
#         ......
#     },
#     {
#         'UserID': 124356363,
#         'UserName':xxxxxx,
#         ......
#     },
#     ......
# ]

add_datas = []

get_datas = []

delet_datas = []

update_datas = []

addlist_datas = []"""

    test_controller = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
from utils.response_code import RET
from .datas import *
from controller.{controllerName}Controller import {controllerClassName}Controller


@pytest.mark.controller
def test_add():
    for data in add_datas:
        result = {controllerClassName}Controller.add(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_get():
    for data in get_datas:
        result = {controllerClassName}Controller.get(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_delet():
    for data in delet_datas:
        result = {controllerClassName}Controller.delete(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_update():
    for data in update_datas:
        result = {controllerClassName}Controller.update(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_addlist():
    for data in addlist_datas:
        result = {controllerClassName}Controller.add_list(**data)
        assert result['code'] == RET.OK"""

    resource_datas = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
# add test_datas here:
# example:
# add_datas = [
#     {
#         'UserID': 123456789,
#         'UserName':xxxxxx,
#         ......
#     },
#     {
#         'UserID': 124356363,
#         'UserName':xxxxxx,
#         ......
#     },
#     ......
# ]

get_data = []

delete_data = []

put_data = []

post_data = []

get_query_data = []

joint_query_data = []"""

    test_resource_utils = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests


def printResponse(response):
    print('\\n\\n------------------------------------------')
    print(response.status_code)

    for k, v in response.headers.items():
        print(f'{k}: {v}')

    print('')

    print(response.content.decode('utf8'))
    print('------------------------------------------\\n\\n')


# 模拟登录,获取token
def get_token(api_url, request_data):
    response = requests.post(api_url,
                             data=request_data
                             )

    response_data_dict = json.loads(response.text)
    token = response_data_dict['data']['Token']
    # printResponse(response)
    print('token:', token)
    return token
    """

    test_resource = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import pytest
from .datas import *
from ..utils import printResponse
from utils.response_code import RET


@pytest.mark.resource
def test_get_{resourceName}Resource():
    api_url = "http://xxxxxx"
    for data in get_data:
        response = requests.get(api_url,
                                params=data,
                                )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK


@pytest.mark.resource
def test_delet_{resourceName}Resource():
    for data in delete_data:
        api_url = ""
        response = requests.delete(api_url,
                                   data=data,
                                   )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK


@pytest.mark.resource
def test_put_{resourceName}Resource():
    for data in put_data:
        api_url = ""
        response = requests.put(api_url,
                                data=data,
                                )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK


@pytest.mark.resource
def test_post_{resourceName}Resource():
    for data in post_data:
        api_url = ""
        response = requests.post(api_url,
                                 data=data,
                                 )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK


@pytest.mark.resource
def test_get_query_{resourceName}Resource():
    for data in get_query_data:
        api_url = ""
        response = requests.get(api_url,
                                params=data,
                                )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK


@pytest.mark.resource
def test_joint_query_{resourceName}Resource():
    for data in joint_query_data:
        api_url = ""
        response = requests.get(api_url,
                                params=data,
                                )
        response.encoding = 'utf8'
        printResponse(response)
        assert json.loads(response.text)['code'] == RET.OK"""
