#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: data_template.py
@time: 2023/4/11 15:44

"""
class DataTemplate:
    delete_yaml = """api_name: {table_name}删除接口
  request:
    method: delete
    url: /api_1_0/{table_name}
    headers:
      token: token
      content-type: application/json
  test_cases:
  - case_name:"your case name1"
    data:
      id: 2024040720004078
    validate:
      eq:
        status_code: 200
        code: "2000"

  - case_name: "your case name2"
    data:
      id: 111
    validate:
      eq:
        status_code: 200
        code: "2000"

    """

    get_yaml = """api_name: {table_name}查询接口
  request:
    method: get
    url: /api_1_0/{table_name}
    headers:
      token: token
  test_cases:
  - case_name:"your case name1"
    data:
      id: 2024040720004078
    validate:
      eq:
        status_code: 200
        code: "2000"

  - case_name: "your case name2"
    data:
      id: 111
    validate:
      eq:
        status_code: 200
        code: "2000"

    """

    post_yaml = """- name: {table_name}添加接口
  request:
    method: post
    url: /api_1_0/{table_name}
    headers:
      token: token
  test_cases:
  - case_name:"your case name1"
    data:
      id: 2024040720004078
    validate:
      eq:
        status_code: 200
        code: "2000"

  - case_name: "your case name2"
    data:
      id: 111
    validate:
      eq:
        status_code: 200
        code: "2000"

    """

    put_yaml = """- name: {table_name}修改接口
  request:
    method: put
    url: /api_1_0/{table_name}
    headers:
      content-type: application/json
  test_cases:
  - case_name:"your case name1"
    data:
      id: 2024040720004078
    validate:
      eq:
        status_code: 200
        code: "2000"

  - case_name: "your case name2"
    data:
      id: 111
    validate:
      eq:
        status_code: 200
        code: "2000"

    """

    service_yaml = """-
  module_name: {table_name}Service
  class_name: {table_name}Service
  function_name: xxx
  params:{data}
  validate:
    - eq:
        - code
        - "2000"
    """


