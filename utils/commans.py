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

from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from sqlacodegen.modelcodegen.codegen import CheckConstraint
from utils.loggings import loggings


def check_config():
    """
    读取并检验参数
    :return: 成功时返回True，失败时返回False
    """
    flag = True
    try:
        loggings.info(1, "开始检验PARAMETER参数")
        # 读取PARAMETER参数
        parameter = {
            'target_dir': Settings.TARGET_DIR,
            'project_name': Settings.PROJECT_NAME,
            'codegen_mode': Settings.CODEGEN_MODE,
            'codegen_layer': Settings.CODEGEN_LAYER,
            'static_resource_dir': Settings.STATIC_RESOURCE_DIR
        }
        for k, v in parameter.items():
            if not v:
                flag = False
                loggings.error(1, '{}参数为空'.format(k))
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    finally:
        loggings.info(1, 'PARAMETER参数检验完成')

    try:
        loggings.info(1, '开始读取DATABASE参数')
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
                loggings.error(1, '{}参数为空'.format(k))
                flag = False
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    finally:
        loggings.info(1, 'DATABASE参数检验完成')

    try:
        if Settings.CODEGEN_LAYER in ['default', 'model']:
            loggings.info(1, '开始检验MODEL参数')
            # 代码生成层级为默认或模型层，读取MODEL参数
            model = {
                'url': Settings.MODEL_URL,
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
            engine = create_engine(model['url'])
            if Settings.CODEGEN_MODE == 'table':
                model['tables'] = Settings.MODEL_TABLES
                if not model['tables']:
                    flag = False
                    loggings.error(1, '{}参数缺失'.format('tables'))
                else:
                    metadata = MetaData(engine)
                    for i in model['tables'].split(','):
                        if i not in metadata.tables.keys():
                            flag = False
                            loggings.error(1, '{}表不存在'.format(i))
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    finally:
        loggings.info(1, 'MODEL参数检验完成')
    try:
        loggings.info(1, '开始检验CONTROLLER参数')
        if Settings.CODEGEN_LAYER in ['default', 'controller']:
            # 代码生成层级为默认或控制器层，读取CONTROLLER参数
            controller = {

            }
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    finally:
        loggings.info(1, 'CONTROLLER参数检验完成')
    try:
        loggings.info(1, '开始检验RESOURCE参数')
        if Settings.CODEGEN_LAYER in ['default', 'resource']:
            # 代码生成层级为默认或接口层，读取RESOURCE参数
            resource = {

            }
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    finally:
        loggings.info(1, 'RESOURCE参数检验完成')
    try:
        loggings.error(1, '开始检验STATIC参数')
        if Settings.CODEGEN_LAYER in ['default', 'static']:
            # 代码生成层级为默认或静态文件层，读取STATIC参数
            static = {

            }
    except Exception as e:
        flag = False
        loggings.error(1, str(e))
    return flag


def get_column_names(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(get_column_names(constraint))
