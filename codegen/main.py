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

import codegen.servicecodegen.main
import codegen.staticcodegen.main
import codegen.controllercodegen.main
import codegen.resourcecodegen.main
import codegen.modelcodegen.main
import codegen.testcodegen.main
from config.setting import Settings

from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


def start(a):
    """
        步骤：
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Service层代码
            四、 生成Resource层代码
            五、 打包静态文件
    """
    url = Settings.MODEL_URL
    engine = create_engine(url)
    metadata = MetaData(engine)
    metadata.reflect(engine, only=Settings.MODEL_TABLES if Settings.MODEL_TABLES else None)

    table_dict = TableMetadata.get_tables_metadata(metadata, a)

    # 第一步
    loggings.info(1, "Start to build the Model layer code, please wait...")
    codegen.modelcodegen.main.main(table_dict)
    loggings.info(1, "Model layer code build completed")

    # 第二步
    loggings.info(1, "Start to build the Controller layer code, please wait...")
    codegen.controllercodegen.main.main(table_dict)
    loggings.info(1, "Controller layer code build completed")

    # 第三步
    loggings.info(1, "Start to build the Service layer code, please wait...")
    codegen.servicecodegen.main.main(table_dict)
    loggings.info(1, "Service layer code build completed")

    # 第四步
    loggings.info(1, "Start to build the Resource layer code, please wait...")
    codegen.resourcecodegen.main.main(table_dict)
    loggings.info(1, "Resource layer code build completed")

    # 第五步
    loggings.info(1, "Start packing static files, please wait...")
    codegen.staticcodegen.main.main()
    loggings.info(1, "Static resource packaging is complete")

    loggings.info(1, "Api project code generation completed")

    # 第六步
    loggings.info(1, "Start to build the Test layer code, please wait...")
    codegen.testcodegen.main.main()
    loggings.info(1, "Test layer code build completed")
