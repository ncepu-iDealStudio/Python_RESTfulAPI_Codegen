#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# author:Nathan
# datetime:2021/8/20 21:35
# software: PyCharm

"""
    this is function description
"""
import json

from sqlalchemy import create_engine, MetaData

import codegen.controllercodegen.main
import codegen.modelcodegen.main
import codegen.resourcecodegen.main
import codegen.servicecodegen.main
import codegen.staticcodegen.main
import codegen.testcodegen.main
from codegen import model_url
from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


def start(table_config):
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
    # 参数初始化
    url = model_url
    engine = create_engine(url)
    metadata = MetaData(engine)
    # table_config = json.loads(table_config)

    metadata.reflect(engine, only=[table['table'] for table in table_config])

    table_dict = TableMetadata.get_tables_metadata(metadata, table_config)

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

    # 第六步
    loggings.info(1, "Start to build the Test layer code, please wait...")
    codegen.testcodegen.main.main(table_dict)
    loggings.info(1, "Test layer code build completed")

    loggings.info(1, "Api project code generation completed")
