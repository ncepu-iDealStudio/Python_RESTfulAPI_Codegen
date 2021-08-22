#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm
"""
this is function description
"""
# import module your need
# In SQLAlchemy 0.x, constraint.columns is sometimes a list, on 1.x onwards, always a
# ColumnCollection

from sqlacodegen.modelcodegen.codegen import CheckConstraint
from config.setting import Settings


def check_config():
    """
    读取并检验参数
    :return:
    {
        'code': 参数检验成功为True,失败为False,
        'message': 提示信息,
        'error': 失败报错，如缺失、错误的参数等,
        'data': 获取的参数
    }
    """
    results = {}

    # 读取PARAMETER参数
    parameter = {
        'source_dir': Settings.SOURCE_DIR,
        'project_name': Settings.PROJECT_NAME,
        'codegen_mode': Settings.CODEGEN_MODE,
        'codegen_layer': Settings.CODEGEN_LAYER,
        'static_resource_dir': Settings.STATIC_RESOURCE_DIR
    }
    for k, v in parameter.items():
        if not v:
            return {'code': False, 'message': '缺少参数{}'.format(k), 'error': '缺少参数{}'.format(k)}
    results['parameter'] = parameter

    # 读取DATABASE参数
    database = {
        'dialect': Settings.DIALECT,
        'driver': Settings.DRIVER,
        'username': Settings.USERNAME,
        'password': Settings.PASSWORD,
        'host': Settings.HOST,
        'port': Settings.PORT,
        'database': Settings.DATABASE,
        'sqlalchemy_track_modifications': Settings.SQLALCHEMY_TRACK_MODIFICATIONS,
        'sqlalchemy_pool_size': Settings.SQLALCHEMY_POOL_SIZE,
        'sqlalchemy_max_overflow': Settings.SQLALCHEMY_MAX_OVERFLOW
    }
    for k, v in database.items():
        if k == 'password':
            continue
        if not v:
            return {'code': False, 'message': '缺少参数{}'.format(k), 'error': '缺少参数{}'.format(k)}
    results['database'] = database

    if parameter['codegen_layer'] in ['default', 'model']:
        # 代码生成层级为默认或模型层，读取MODEL参数
        model = {
            'version': Settings.MODEL_VERSION,
            'schema': Settings.MODEL_SCHEMA,
            'noviews': Settings.MODEL_NOVIEWS,
            'noindexes': Settings.MODEL_NOINDEXES,
            'noconstraints': Settings.MODEL_NOCONSTRAINTS,
            'nojoied': Settings.MODEL_NOJOINED,
            'noinflect': Settings.MODEL_NOINFLECT,
            'noclasses': Settings.MODEL_NOCLASSES,
            'nocomments': Settings.MODEL_NOCOMMENTS,
            'outfile': Settings.MODEL_OUTFILE
        }
        if parameter.get('codegen_mode') == 'table':
            model['tables'] = Settings.MODEL_TABLES
            if not model['tables']:
                return {'code': False, 'message': '缺少参数tables', 'error': '缺少参数tables'}
        results['model'] = model
    if parameter['codegen_layer'] in ['default', 'controller']:
        # 代码生成层级为默认或控制器层，读取CONTROLLER参数
        controller = {

        }
        results['controller'] = controller
    if parameter['codegen_layer'] in ['default', 'resource']:
        # 代码生成层级为默认或接口层，读取RESOURCE参数
        resource = {

        }
        results['resource'] = resource
    return {'code': True, 'message': '参数读取检验成功', 'data': results}


def get_column_names(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(get_column_names(constraint))
