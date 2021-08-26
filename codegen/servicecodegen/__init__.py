#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:Nathan
# datetime:2021/8/26 10:58
# software: PyCharm

"""
    this is function description
"""

import os

from sqlalchemy import create_engine, MetaData

from config.setting import Settings
from utils.checkTable import CheckTable

url = Settings.MODEL_URL
schema = Settings.MODEL_SCHEMA
tables = CheckTable.check_primary_key()
noviews = Settings.MODEL_NOVIEWS
project_dir = Settings.PROJECT_DIR

# Use reflection to fill in the metadata
engine = create_engine(url)
metadata = MetaData(engine)

metadata.reflect(engine, schema, not noviews, tables)

# Create folder named "service" in project directory
os.makedirs(service_path := os.path.join(project_dir, 'service'), exist_ok=True)
with open(os.path.join(service_path, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write("#!/usr/bin/env python\n# -*- coding:utf-8 -*-\n")
