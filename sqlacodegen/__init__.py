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
CONFIG = ConfigParser(allow_no_value=True)
CONFIG.read(os.path.join(CONFIG_DIR, 'config.conf'), encoding='utf-8')


def modelGenerate():
    """
    model层代码的生成
    :return: None
    """
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
    generator.render(outfile)
    return


def controllerGenerate():
    """
    生成Controller层代码
    :return: None
    """
    pass


def resourceGenerate():
    """
    生成Resource层代码层代码
    :return: None
    """
    pass


def staticGenerate():
    """
    打包静态文件
    :return: None
    """
    pass
