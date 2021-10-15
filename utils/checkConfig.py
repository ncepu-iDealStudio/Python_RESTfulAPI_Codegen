#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkConfig.py
# author:Itsuka
# datetime:2021/8/23 15:12
# software: Pycharm

"""
    检验配置文件
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
        loggings.info(1, "Start checking the necessary parameters, please wait ...")
        # 读取PARAMETER参数
        parameter = {
            'target_dir': Settings.TARGET_DIR,
            'project_name': Settings.PROJECT_NAME,
            'codegen_mode': Settings.CODEGEN_MODE,
            'codegen_layer': Settings.CODEGEN_LAYER,
            'static_resource_dir': Settings.STATIC_RESOURCE_DIR,
            # 'primary_key': Settings.PRIMARY_KEY
        }
        for key, value in parameter.items():
            if not value:
                raise Exception('{}参数为空'.format(key))

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
        for key, value in database.items():
            if key == 'password':
                continue
            if not value:
                raise Exception('{}参数为空'.format(key))

        # 读取MODEL参数
        if Settings.CODEGEN_LAYER in ['default', 'model']:
            # 代码生成层级为默认或模型层，读取MODEL参数
            model = {
                'url': Settings.MODEL_URL
            }

            if not model['url']:
                raise Exception('{}参数缺失'.format('url'))

            if Settings.CODEGEN_MODE == 'table' and not Settings.MODEL_TABLES:
                raise Exception('{}参数缺失'.format('tables'))

        # 读取CONTROLLER参数
        if Settings.CODEGEN_LAYER in ['default', 'model']:
            # 代码生成层级为默认或控制器层
            controller = {
                # 'record_delete_way': Settings.CONTROLLER_RECORD_DELETE_WAY
            }
            # for key, value in controller.items():
            #     if not value:
            #         raise Exception('{}参数缺失'.format(key))
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
    except Exception as e:
        loggings.error(1, str(e))
        return False

    # 检验参数逻辑
    try:
        loggings.info(1, 'Please wait a moment to verify the parameter logic ...')

        # 检验参数值合法与否
        if Settings.CODEGEN_MODE not in ['database', 'table']:
            raise Exception('CODEGEN_MODE参数值不合法')
        if Settings.CODEGEN_LAYER not in ['default', 'model', 'controller', 'resource', 'static']:
            raise Exception('CODEGEN_LAYER参数值不合法')
        # if Settings.CODEGEN_LAYER in ['default', 'controller']:
        #     if Settings.CONTROLLER_RECORD_DELETE_WAY not in ['logic', 'physical']:
        #         raise Exception('RECORD_DELETE_WAY参数值不合法')
        # if Settings.PRIMARY_KEY not in ['AutoID', 'DoubleKey']:
        #     raise Exception('PRIMARY_KEY参数值不合法')

        engine = create_engine(Settings.MODEL_URL)
        metadata = MetaData(engine)
        metadata.reflect(engine)

        table_rule = Settings.TABLE_RULE

        if Settings.CODEGEN_MODE == 'table':
            # 检验数据库中是否存在参数中的表名
            tables = Settings.MODEL_TABLES.replace(' ', '').split(',')
            for i in tables:
                if i not in metadata.tables.keys():
                    raise Exception('The table {} does not exist'.format(i))
            # 检查table_rule配置文件中各表是否存在
            for table in table_rule['table_record_delete_logic_way']:
                if table not in tables:
                    loggings.warning(1, 'The table {} to be logically deleted is not in the table to be generated, '
                                        'please check the table_rule profile'.format(table))
            for table in table_rule['table_business_key_gen_rule'].keys():
                if table not in tables:
                    loggings.warning(1, 'The table {} to set the business key is not in the table to be generated, '
                                        'please check the table_rule profile'.format(table))
        else:
            # 检查table_rule配置文件中各表是否存在
            for table in table_rule['table_record_delete_logic_way']:
                if table not in metadata.tables.keys():
                    loggings.warning(1, 'The table deletion {} for logical deletion does not exist. Please check '
                                        'table_rule profile'.format(table))
            for table in table_rule['table_business_key_gen_rule'].keys():
                if table not in metadata.tables.keys():
                    loggings.warning(1, 'The table {} to set the business primary key does not exist, please check '
                                        'the table_rule profile'.format(table))

    except Exception as e:
        loggings.error(1, str(e))
        return False

    return True
