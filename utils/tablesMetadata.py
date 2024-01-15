#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:tablesMetadata.py.py
# author:Nathan
# datetime:2021/8/26 14:56
# software: PyCharm

"""
    Get metadata of all tables
"""
import json
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from sqlalchemy.engine import reflection

from utils.common import str_to_all_small, str_to_little_camel_case, str_to_big_camel_case, standard_str


class TableMetadata(object):
    with open('config/default_table_config.json', 'r', encoding='utf-8') as f:
        DEFAULT_CONFIG = f.read()

    with open('config/datatype_map.json', 'r', encoding='utf-8') as f:
        TYPE_MAPPING = json.load(f)

    @classmethod
    def get_tables_metadata(cls, metadata, reflection_views, table_config=DEFAULT_CONFIG) -> dict:
        """
            获取数据库表数据
            :param metadata: sqlalchemy元数据
            :param table_config: 表配置
        """

        table_config = table_config if isinstance(table_config, dict) else json.loads(table_config)

        # Get all tables object
        table_objs = metadata.tables.values()
        table_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        # Using multithreading to speed up the convert process
        pool = ThreadPool(2 * cpu_count() + 1)
        for table in table_objs:
            if str(table) not in reflection_views:
                pool.apply_async(cls.metadata_tables_transition, (table_config, metadata, table, table_dict))
                # pool.apply_async(cls.metadata_tables_transition_update, (table_config, metadata, table, table_dict))
        pool.close()
        pool.join()

        return table_dict

    @classmethod
    def get_tables_metadata_update(cls, metadata, reflection_views, table_config=DEFAULT_CONFIG) -> dict:
        """
            获取数据库表数据
            :param metadata: sqlalchemy元数据
            :param table_config: 表配置
        """

        table_config = table_config if isinstance(table_config, dict) else json.loads(table_config)

        # Get all tables object
        # table_objs = metadata.tables.values()
        table_objs = metadata.tables
        table_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        # Using multithreading to speed up the convert process
        pool = ThreadPool(2 * cpu_count() + 1)
        for table_name,table in table_objs.items():
            if str(table) not in reflection_views:
                # pool.apply_async(cls.metadata_tables_transition, (table_config, metadata, table, table_dict))
                pool.apply_async(cls.metadata_tables_transition_update,(table_config,table_name, metadata, table, table_dict))
        pool.close()
        pool.join()

        return table_dict

    @classmethod
    def get_views_metadata(cls, metadata, reflection_views, table_config=DEFAULT_CONFIG) -> dict:
        """
            获取数据库视图数据
            :param metadata: sqlalchemy元数据
            :param table_config: 表配置
        """

        table_config = table_config if isinstance(table_config, dict) else json.loads(table_config)

        # Get all tables object
        view_objs = metadata.tables.values()
        view_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        # Using multithreading to speed up the convert process
        pool = ThreadPool(2 * cpu_count() + 1)
        for view in view_objs:
            if str(view) in reflection_views:
                pool.apply_async(cls.metadata_views_transition, (table_config, metadata, view, view_dict))
        pool.close()
        pool.join()

        return view_dict

    @classmethod
    def get_views_metadata_update(cls, metadata, reflection_views,inspector, table_config=DEFAULT_CONFIG) -> dict:
        """
            获取数据库视图数据
            :param metadata: sqlalchemy元数据
            :param table_config: 表配置
        """

        table_config = table_config if isinstance(table_config, dict) else json.loads(table_config)

        # Get all tables object
        view_objs = reflection_views
        view_dict = {}

        # Traverse each table object to get corresponding attributes to form an attribute dictionary
        # Using multithreading to speed up the convert process
        pool = ThreadPool(2 * cpu_count() + 1)
        for view in view_objs:
            if str(view) in reflection_views:
                pool.apply_async(cls.metadata_views_transition_update,(table_config, metadata, inspector, view,view_dict))
        pool.close()
        pool.join()

        return view_dict

    @classmethod
    def metadata_tables_transition(cls, table_config, metadata, table, table_dict):
        """
            数据库表元数据转换
            :param table_config 表配置
            :param metadata sqlalchemy元数据
            :param table 待转换的表数据
            :param table_dict 数据库数据汇总字典
        """
        table_name = str(table)
        table_dict[table_name] = {}
        table_dict[table_name]['table_name'] = table_name
        table_dict[table_name]['table_name_all_small'] = str_to_all_small(table_name)
        table_dict[table_name]['table_name_little_camel_case'] = str_to_little_camel_case(table_name)
        table_dict[table_name]['table_name_big_camel_case'] = str_to_big_camel_case(table_name)
        table_dict[table_name]['table_name_api_standard'] = standard_str(table_name)
        table_dict[table_name]['is_view'] = False
        table_dict[table_name]['logical_delete_column'] = ""
        table_dict[table_name]['business_key_column'] = {}

        # Check if the business key exists and check record deletion method
        for config in table_config['table']:
            if config['table'] == table_name and config['logicaldeletemark'] != '':
                table_dict[table_name]['logical_delete_column'] = config['logicaldeletemark']

            if config['table'] == table_name and config['businesskeyname'] != '':
                table_dict[table_name]['business_key_column']['column'] = config['businesskeyname']
                table_dict[table_name]['business_key_column']['rule'] = config['businesskeyrule']

        # 需要加密的字段和敏感修改的字段
        table_dict[table_name]['rsa_columns'] = []
        table_dict[table_name]['aes_columns'] = []
        table_dict[table_name]['sensitive_columns'] = []

        for one_table in table_config['table']:
            if one_table['table'] == table_name:
                for one_colume in one_table['field']:

                    # 属于敏感字段
                    if one_colume.get('field_sensitive', None):
                        table_dict[table_name]['sensitive_columns'].append(one_colume['field_name'])

                    # 需要加密
                    if one_colume['field_encrypt']:

                        # 加密方式为rsa
                        if one_colume['encrypt_type'] == 'rsa':
                            table_dict[table_name]['rsa_columns'].append(one_colume['field_name'])

                        # 加密方式为aes
                        elif one_colume['encrypt_type'] == 'aes':
                            table_dict[table_name]['aes_columns'].append(one_colume['field_name'])

        insp = reflection.Inspector.from_engine(metadata.bind)

        # 初始化为空列表
        table_dict[table_name]['primary_key_columns'] = insp.get_pk_constraint(table_name)['constrained_columns']
        table_dict[table_name]['columns'] = {}

        # Traverse each columns to get corresponding attributes
        for column in table.columns.values():
            table_dict[table_name]['columns'][str(column.name)] = {}
            table_dict[table_name]['columns'][str(column.name)]['name'] = str(column.name)

            for type_ in cls.TYPE_MAPPING:
                if str(metadata.bind.url).split('+')[0] != type_['database']:
                    continue
                for python_type, sql_type_list in type_['data_map'].items():
                    if str(column.type).lower() in sql_type_list:
                        table_dict[table_name]['columns'][str(column.name)]['type'] = python_type
                        break
            table_dict[table_name]['columns'][str(column.name)].setdefault('type', 'str')

            # 是否自动递增
            table_dict[table_name]['columns'][str(column.name)][
                'is_autoincrement'] = True if column.autoincrement is True else False

            # 存在复合主键
            if len(table_dict[table_name]['primary_key_columns']) > 1:
                table_dict[table_name]['business_key_column'] = {}
            else:
                # 如果主键不是自增的，则将业务主键设置为主键
                if str(column.name) in table_dict[table_name]['primary_key_columns'] and not \
                        table_dict[table_name]['columns'][str(column.name)]['is_autoincrement']:
                    table_dict[table_name]['business_key_column']['column'] = str(column.name)

            # 是否可以为空
            table_dict[table_name]['columns'][str(column.name)]['nullable'] = column.nullable

            # 是否存在默认值
            table_dict[table_name]['columns'][str(column.name)][
                'is_exist_default'] = True if column.server_default is not None else False

    @classmethod
    def metadata_tables_transition_update(cls, table_config,table_name, metadata, table, table_dict):
        """
            数据库表元数据转换
            :param table_config 表配置
            :param metadata sqlalchemy元数据
            :param table 待转换的表数据
            :param table_dict 数据库数据汇总字典
        """
        table_name = table_name
        table_dict[table_name] = {}
        table_dict[table_name]['table_name'] = table_name
        table_dict[table_name]['table_name_all_small'] = str_to_all_small(table_name)
        table_dict[table_name]['table_name_little_camel_case'] = str_to_little_camel_case(table_name)
        table_dict[table_name]['table_name_big_camel_case'] = str_to_big_camel_case(table_name)
        table_dict[table_name]['table_name_api_standard'] = standard_str(table_name)
        table_dict[table_name]['is_view'] = False
        table_dict[table_name]['logical_delete_column'] = ""
        table_dict[table_name]['business_key_column'] = {}

        # Check if the business key exists and check record deletion method
        for config in table_config['table']:
            if config['table'] == table_name and config['logicaldeletemark'] != '':
                table_dict[table_name]['logical_delete_column'] = config['logicaldeletemark']

            if config['table'] == table_name and config['businesskeyname'] != '':
                table_dict[table_name]['business_key_column']['column'] = config['businesskeyname']
                table_dict[table_name]['business_key_column']['rule'] = config['businesskeyrule']

        # 需要加密的字段和敏感修改的字段
        table_dict[table_name]['rsa_columns'] = []
        table_dict[table_name]['aes_columns'] = []
        table_dict[table_name]['sensitive_columns'] = []

        for one_table in table_config['table']:
            if one_table['table'] == table_name:
                for one_colume in one_table['field']:

                    # 属于敏感字段
                    if one_colume.get('field_sensitive', None):
                        table_dict[table_name]['sensitive_columns'].append(one_colume['field_name'])

                    # 需要加密
                    if one_colume['field_encrypt']:

                        # 加密方式为rsa
                        if one_colume['encrypt_type'] == 'rsa':
                            table_dict[table_name]['rsa_columns'].append(one_colume['field_name'])

                        # 加密方式为aes
                        elif one_colume['encrypt_type'] == 'aes':
                            table_dict[table_name]['aes_columns'].append(one_colume['field_name'])

        # insp = reflection.Inspector.from_engine(metadata.bind)

        # 初始化为空列表
        table_dict[table_name]['columns'] = {}
        table_dict[table_name]['primary_key_columns'] = []

        # all_tables = metadata.tables

        # # 遍历所有表
        # for table_name, table in all_tables.items():
        #     # 获取所有列的信息
        for column in table.c:
            # 示例：输出列名和类型
            table_dict[table_name]['columns'][str(column.name)] = {}
            table_dict[table_name]['columns'][str(column.name)] = {
                'name': str(column.name),
                'type': str(column.type),
                'is_autoincrement': column.autoincrement if column.autoincrement is not None else False,
                'nullable': column.nullable,
                'is_exist_default': column.server_default is not None
            }
            # 存在复合主键
            if table.primary_key:
                # 获取主键包含的列
                table_dict[table_name]['primary_key_columns'] = [column.name for column in
                                                                       table.primary_key.columns]
                if len(table.primary_key) > 1:
                    table_dict[table_name]['business_key_column'] = {}

                else:
                    # 如果主键不是自增的，则将业务主键设置为主键
                    column_name = table_dict[table_name]['primary_key_columns'][0]
                    column = table.columns[column_name]
                    is_autoincrement = column.autoincrement if column.autoincrement is not None else False
                    # 如果不是自增，设置为业务主键
                    if not is_autoincrement:
                        table_dict[table_name]['business_key_column'] = {'column': column_name}

    @classmethod
    def metadata_views_transition(cls, table_config, metadata, table, table_dict):
        """
            数据库视图元数据转换
            :param table_config 表配置
            :param metadata sqlalchemy元数据
            :param table 待转换的表数据
            :param table_dict 数据库数据汇总字典
        """
        table_name = str(table)
        table_dict[table_name] = {}
        table_dict[table_name]['table_name'] = table_name
        table_dict[table_name]['table_name_all_small'] = str_to_all_small(table_name)
        table_dict[table_name]['table_name_little_camel_case'] = str_to_little_camel_case(table_name)
        table_dict[table_name]['table_name_big_camel_case'] = str_to_big_camel_case(table_name)
        table_dict[table_name]['table_name_api_standard'] = standard_str(table_name)
        table_dict[table_name]['is_view'] = True
        table_dict[table_name]['filter_field'] = []

        # 遍历所有的视图配置
        for view in table_config['view']:
            if table_name == view['view']:
                # 遍历配置中的字段
                for field in view['filter_field']:
                    # 如果字段被勾选，则将字段名称和类型添加进字典中
                    if field['ischecked']:
                        table_dict[table_name]['filter_field'].append({
                            "field_name": field['field_name'],
                            "field_type": field['field_type']
                        })

        table_dict[table_name]['columns'] = []
        for column in table.columns.values():
            temp_column_dict = {
                "field_name": str(column.name),
            }

            for type_ in cls.TYPE_MAPPING:
                if str(metadata.bind.url).split('+')[0] != type_['database']:
                    continue
                for python_type, sql_type_list in type_['data_map'].items():
                    if str(column.type).lower() in sql_type_list:
                        temp_column_dict['field_type'] = python_type
                        break

            temp_column_dict.setdefault('field_type', 'str')
            table_dict[table_name]['columns'].append(temp_column_dict)

    @classmethod
    def metadata_views_transition_update(cls, table_config, metadata,inspector, table, table_dict):
        """
            数据库视图元数据转换
            :param table_config 表配置
            :param metadata sqlalchemy元数据
            :param table 待转换的表数据
            :param table_dict 数据库数据汇总字典
        """
        table_name = str(table)
        table_dict[table_name] = {}
        table_dict[table_name]['table_name'] = table_name
        table_dict[table_name]['table_name_all_small'] = str_to_all_small(table_name)
        table_dict[table_name]['table_name_little_camel_case'] = str_to_little_camel_case(table_name)
        table_dict[table_name]['table_name_big_camel_case'] = str_to_big_camel_case(table_name)
        table_dict[table_name]['table_name_api_standard'] = standard_str(table_name)
        table_dict[table_name]['is_view'] = True
        table_dict[table_name]['filter_field'] = []

        # 遍历所有的视图配置
        for view in table_config['view']:
            if table_name == view['view']:
                # 遍历配置中的字段
                for field in view['filter_field']:
                    # 如果字段被勾选，则将字段名称和类型添加进字典中
                    if field['ischecked']:
                        table_dict[table_name]['filter_field'].append({
                            "field_name": field['field_name'],
                            "field_type": field['field_type']
                        })
        # 创建一个列表用于存储视图字段信息
        table_dict[table_name]['columns'] = []

        # # 遍历每个视图
        # for view_name in table:
        #     # 获取视图的列信息
        columns = inspector.get_columns(table)

        # 遍历每个列，并将字段信息添加到列表中
        for column in columns:
            field_info = {
                'field_name': column['name'],
                'field_type': str(column['type'])
            }
            table_dict[table_name]['columns'].append(field_info)

        # # 输出视图字段信息
        # print(views_info)

