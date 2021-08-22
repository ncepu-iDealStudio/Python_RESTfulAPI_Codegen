#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file:start.py
# author:张仁
# datetime:2021/8/20 21:35
# software: PyCharm
"""
    this is function description
"""

from __future__ import unicode_literals, division, print_function, absolute_import

import io
import os
import sys
from configparser import ConfigParser

import pkg_resources
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from sqlacodegen.modelcodegen.codegen import CodeGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
CONFIG = ConfigParser()
CONFIG.read(os.path.join(CONFIG_DIR, 'config.ini'), encoding='utf-8')


def main():
    # 接收参数
    url = CONFIG['PARAM']['URL'] if CONFIG['PARAM']['URL'] else None
    # version = CONFIG['PARAM']['VERSION'] if CONFIG['PARAM']['VERSION'] else None
    # schema = CONFIG['PARAM']['SCHEMA'] if CONFIG['PARAM']['SCHEMA'] else None
    tables = CONFIG['PARAM']['TABLES'] if CONFIG['PARAM']['TABLES'] else None
    # noviews = CONFIG['PARAM']['NOVIEWS'] if CONFIG['PARAM']['NOVIEWS'] else None
    # noindexes = CONFIG['PARAM']['NOINDEXES'] if CONFIG['PARAM']['NOINDEXES'] else None
    # noconstraints = CONFIG['PARAM']['NOCONSTRAINTS'] if CONFIG['PARAM']['NOCONSTRAINTS'] else None
    # nojoined = CONFIG['PARAM']['NOJOINED'] if CONFIG['PARAM']['NOJOINED'] else None
    # noinflect = CONFIG['PARAM']['NOINFLECT'] if CONFIG['PARAM']['NOINFLECT'] else None
    # noclasses = CONFIG['PARAM']['NOCLASSES'] if CONFIG['PARAM']['NOCLASSES'] else None
    # nocomments = CONFIG['PARAM']['NOCOMMENTS'] if CONFIG['PARAM']['NOCOMMENTS'] else None
    outfile = CONFIG['PARAM']['OUTFILE'] if CONFIG['PARAM']['OUTFILE'] else None

    if None:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return

    if not url:
        print('You must supply a url\n', file=sys.stderr)
        return

        # Use reflection to fill in the metadata
    # 返回Engine实例，直到触发数据库事件时才真正去连接数据库
    engine = create_engine(url)
    # 获得所有Table对象的集合
    metadata = MetaData(engine)
    # 获得需要生成model的表名列表
    tables = tables.split(',') if tables else None

    # 临时创建的比变量：
    schema = None
    noviews = False
    noindexes = False
    noconstraints = False
    nojoined = False
    noinflect = False
    noclasses = False
    nocomments = False
    metadata.reflect(engine, schema, not noviews, tables)

    # Write the generated model code to the specified file or standard output
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout

    # model代码生成
    generator = CodeGenerator(metadata, noindexes, noconstraints, nojoined,
                              noinflect, noclasses, nocomments=nocomments)

    print("successful")
    generator.render(outfile)


from sqlacodegen.controllercodegen import controllerGenerate
from sqlacodegen.modelcodegen import modelGenerate
from sqlacodegen.resourcecodegen import resourceGenerate
from sqlacodegen.staticcodegen import staticGenerate


if __name__ == '__main__':
    """
        步骤：
            一、 生成Model层代码
            二、 生成Controller层代码
            三、 生成Resource层代码
            四、 打包静态文件
            五、 目标项目启动
            六、 目标项目接口测试
    """

    # 第一步
    print("开始构建Model层代码, 请稍等...")
    modelGenerate()
    print("构建Model层代码完成")

    # 第二步
    print("开始构建Controller层代码, 请稍等...")
    controllerGenerate()
    print("构建Controller层代码完成")

    # 第三步
    print("开始构建Resource层代码, 请稍等...")
    resourceGenerate()
    print("构建Resource层代码完成")

    # 第四步
    print("开始打包静态文件, 请稍等...")
    staticGenerate()
    print("打包静态文件完成")

    print("生成完成")
