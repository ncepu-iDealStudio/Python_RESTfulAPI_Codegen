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

import argparse
import io
import sys

import pkg_resources
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from sqlacodegen.codegen import CodeGenerator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates SQLAlchemy model code from an existing database.')

    args = parser.parse_args()

    if args.version:
        version = pkg_resources.get_distribution('sqlacodegen').parsed_version
        print(version.public)
        return
    if not args.url:
        print('You must supply a url\n', file=sys.stderr)
        parser.print_help()
        return

    # Use reflection to fill in the metadata
    engine = create_engine(args.url)
    metadata = MetaData(engine)
    tables = args.tables.split(',') if args.tables else None
    metadata.reflect(engine, args.schema, not args.noviews, tables)

    # Write the generated model code to the specified file or standard output
    outfile = io.open(args.outfile, 'w', encoding='utf-8') if args.outfile else sys.stdout
    generator = CodeGenerator(metadata, args.noindexes, args.noconstraints, args.nojoined,
                              args.noinflect, args.noclasses, nocomments=args.nocomments)
    generator.render(outfile)