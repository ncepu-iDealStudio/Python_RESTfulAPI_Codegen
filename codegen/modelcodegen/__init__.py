# import argparse
import sys
from contextlib import ExitStack

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from config.setting import Settings

if sys.version_info < (3, 8):
    from importlib_metadata import entry_points, version
else:
    from importlib.metadata import entry_points, version


def modelGenerate() -> None:
    generation_way = {
        'tables': 'tables = sqlacodegen.generators: TablesGenerator',
        'declarative': 'declarative = sqlacodegen.generators:DeclarativeGenerator',
        'dataclasses': 'dataclasses = sqlacodegen.generators:DataclassGenerator'
    }
    # generators = {ep.name: ep for ep in entry_points()['sqlacodegen.generators']}
    generators = {name: value for name, value in generation_way.items()}
    # parser = argparse.ArgumentParser(
    #     description='Generates SQLAlchemy model code from an existing database.')
    # parser.add_argument('url', nargs='?', help='SQLAlchemy url to the database')
    # parser.add_argument('--option', nargs='*', help="options passed to the generator class")
    # parser.add_argument('--version', action='store_true', help="print the version number and exit")
    # parser.add_argument('--schemas', help='load tables from the given schemas (comma separated)')
    # parser.add_argument('--generator', choices=generators, default='declarative',
    #                     help="generator class to use")
    # parser.add_argument('--tables', help='tables to process (comma-separated, default: all)')
    # parser.add_argument('--noviews', action='store_true', help="ignore views")
    # parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    # args = parser.parse_args()

    url = Settings.MODEL_URL
    sqlacodegen_version = Settings.MODEL_VERSION
    schemas = Settings.MODEL_SCHEMA
    tables = Settings.MODEL_TABLES
    noviews = Settings.MODEL_NOVIEWS
    generator = 'declarative'
    option = None
    outfile = Settings.MODEL_OUTFILE
    # codegen_mode = Settings.CODEGEN_MODE

    if sqlacodegen_version:
        print(version('sqlacodegen'))
        return
    if not url:
        print('You must supply a url\n', file=sys.stderr)
        # parser.print_help()
        return

    # Use reflection to fill in the metadata
    engine = create_engine(url)
    metadata = MetaData()
    tables = tables.split(',') if tables else None
    schemas = schemas.split(',') if schemas else [None]
    for schema in schemas:
        metadata.reflect(engine, schema, not noviews, tables)

    # Instantiate the generator
    generator_class = generators[generator].load()
    generator = generator_class(metadata, engine, set(option or ()))

    # Open the target file (if given)
    with ExitStack() as stack:
        if outfile:
            outfile = open(outfile, 'w', encoding='utf-8')
            stack.enter_context(outfile)
        else:
            outfile = sys.stdout

        # Write the generated model code to the specified file or standard output
        outfile.write(generator.generate())
