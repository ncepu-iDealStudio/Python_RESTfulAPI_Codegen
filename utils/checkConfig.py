#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkConfig.py
# author:Itsuka
# datetime:2021/8/23 15:12
# software: Pycharm

"""
    this is function description
"""
from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from utils.loggings import loggings


def check_config():
    """
    读取并检验参数
    :return: 成功时返回True，失败时返回False
    """

    # 检验必要参数
    try:
        loggings.info(1, "开始检验必要参数，请稍等...")
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
                raise Exception('{}参数为空'.format(k))

        # 读取DATABASE参数
        database = {
            'dialect': Settings.DIALECT,
            'driver': Settings.DRIVER,
            'username': Settings.USERNAME,
            'password': Settings.PASSWORD,
            'host': Settings.HOST,
            'port': Settings.PORT,
            'database': Settings.DATABASE_TYPE,
            'sqlalchemy_track_modifications': Settings.SQLALCHEMY_TRACK_MODIFICATIONS,
            'sqlalchemy_pool_size': Settings.SQLALCHEMY_POOL_SIZE,
            'sqlalchemy_max_overflow': Settings.SQLALCHEMY_MAX_OVERFLOW
        }
        for k, v in database.items():
            if k == 'password':
                continue
            if not v:
                raise Exception('{}参数为空'.format(k))

        # 读取MODEL参数
        if Settings.CODEGEN_LAYER in ['default', 'model']:
            # 代码生成层级为默认或模型层，读取MODEL参数
            model = {
                'url': Settings.MODEL_URL,
                'outfile': Settings.MODEL_OUTFILE
            }
            for i in ['url', 'outfile']:
                if not model[i]:
                    raise Exception('{}参数缺失'.format(i))
            if Settings.CODEGEN_MODE == 'table' and not Settings.MODEL_TABLES:
                raise Exception('{}参数缺失'.format('tables'))

        # 读取CONTROLLER参数
        if Settings.CODEGEN_LAYER in ['default', 'model']:
            # 代码生成层级为默认或控制器层
            controller = {

            }

        # 读取RESOURCE参数
        if Settings.CODEGEN_LAYER in ['default', 'resource']:
            # 代码生成层级为默认或接口层，读取RESOURCE参数
            resource = {

            }

        # 读取STATIC参数
        if Settings.CODEGEN_LAYER in ['default', 'static']:
            # 代码生成层级为默认或静态文件层，读取STATIC参数
            static = {

            }
        loggings.info(1, '必要参数检验完成')
    except Exception as e:
        loggings.error(1, str(e))
        return False

    # 检验参数逻辑
    try:
        loggings.info(1, '开始检验参数逻辑，请稍等...')

        # 检验参数值合法与否
        if Settings.CODEGEN_MODE not in ['database', 'table']:
            raise Exception('CODEGEN_MODE参数值不合法')
        if Settings.CODEGEN_LAYER not in ['default', 'model', 'controller', 'resource', 'static']:
            raise Exception('CODEGEN_LAYER参数值不合法')

        # 检验数据库中是否存在参数中的表名
        if Settings.CODEGEN_MODE == 'table':
            engine = create_engine(Settings.MODEL_URL)
            metadata = MetaData(engine)
            metadata.reflect(engine)
            for i in Settings.MODEL_TABLES.replace(' ', '').split(','):
                if i not in metadata.tables.keys():
                    raise Exception('{}表不存在'.format(i))

        loggings.info(1, '参数值逻辑检验完成')
    except Exception as e:
        loggings.error(1, str(e))
        return False

    return True
