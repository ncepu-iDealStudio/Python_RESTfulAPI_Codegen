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

from sqlacodegen.codegen import CodeGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
CONFIG = ConfigParser()
CONFIG.read(os.path.join(CONFIG_DIR, 'config.ini'), encoding='utf-8')


def main():
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
    engine = create_engine(url)
    metadata = MetaData(engine)
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
    generator = CodeGenerator(metadata, noindexes, noconstraints, nojoined,
                              noinflect, noclasses, nocomments=nocomments)

    print("successful")
    generator.render(outfile)


if __name__ == '__main__':
    main()
