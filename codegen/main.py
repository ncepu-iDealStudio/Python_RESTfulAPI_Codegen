#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:Nathan
# datetime:2021/8/20 21:35
# software: PyCharm

"""
    this is function description
"""

from sqlalchemy import create_engine, MetaData

import codegen.controllercodegen.main
import codegen.modelcodegen.main
import codegen.resourcecodegen.main
import codegen.servicecodegen.main
import codegen.staticcodegen.main
import codegen.testcodegen.main

from utils.loggings import loggings
from utils.response_code import RET, error_map
from utils.tablesMetadata import TableMetadata


def start(table_config, session_id, ip):
    """
        步骤：
            零、 获取新的table_dict的值
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Service层代码
            四、 生成Resource层代码
            五、 打包静态文件
            六、 生成test层代码
    """
    try:
        # 初始化配置文件
        from config.setting import Settings
        settings = Settings(session_id)

        # 参数初始化
        engine = create_engine(settings.MODEL_URL)
        metadata = MetaData(engine)

        reflection_tables = [table['table'] for table in table_config['table']]
        reflection_views = [view['view'] for view in table_config['view']]
        metadata.reflect(engine, only=reflection_tables + reflection_views, views=True)

        table_dict = TableMetadata.get_tables_metadata(
            metadata=metadata,
            reflection_views=reflection_views,
            table_config=table_config
        )

        view_dict = TableMetadata.get_views_metadata(
            metadata=metadata,
            reflection_views=reflection_views,
            table_config=table_config
        )

        table_dict = dict(table_dict, **view_dict)

        # 第一步
        loggings.info(1, "Start to build the Model layer code, please wait...", session_id, ip)

        codegen.modelcodegen.main.main(table_dict, settings, session_id, ip)
        loggings.info(1, "Model layer code build completed", session_id, ip)

        # 第二步
        loggings.info(1, "Start to build the Controller layer code, please wait...", session_id, ip)
        codegen.controllercodegen.main.main(table_dict, settings, session_id, ip)
        loggings.info(1, "Controller layer code build completed", session_id, ip)

        # 第三步
        loggings.info(1, "Start to build the Service layer code, please wait...", session_id, ip)
        codegen.servicecodegen.main.main(table_dict, settings, session_id, ip)
        loggings.info(1, "Service layer code build completed", session_id, ip)

        # 第四步
        loggings.info(1, "Start to build the Resource layer code, please wait...", session_id, ip)
        codegen.resourcecodegen.main.main(table_dict, settings, session_id, ip)
        loggings.info(1, "Resource layer code build completed", session_id, ip)

        # 第五步
        loggings.info(1, "Start packing static files, please wait...", session_id, ip)
        codegen.staticcodegen.main.main(settings, session_id, ip)
        loggings.info(1, "Static resource packaging is complete", session_id, ip)

        # 第六步
        loggings.info(1, "Start to build the Test layer code, please wait...", session_id, ip)
        codegen.testcodegen.main.main(table_dict, settings, session_id, ip)
        loggings.info(1, "Test layer code build completed", session_id, ip)

        loggings.info(1, "Api project code generation completed", session_id, ip)

        if session_id and ip:
            log_path = "logs/log_user_info/codegen_log_{user_ip}_{session_id}.log".format(
                    user_ip=ip, session_id=session_id)
        else:
            log_path = "logs/codegen_log.log"
        with open(log_path, 'r', encoding='utf-8') as f:
            result = f.read()

        return {'code': RET.OK, 'message': error_map[RET.OK], 'data': result}

    except Exception as e:
        return {'code': RET.UNKOWNERR, 'message': error_map[RET.UNKOWNERR], 'error': str(e)}
