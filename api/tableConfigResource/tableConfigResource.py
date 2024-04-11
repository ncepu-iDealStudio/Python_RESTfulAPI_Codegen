#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:tablesResource.py
# author:jackiex
# datetime:2024/1/15 17:16
# software: PyCharm

'''
    this is function  description 
'''
import json
import keyword
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count

from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base

from utils.response_code import RET
from utils.loggings import loggings

from utils.common import str_to_all_small, str_to_little_camel_case, str_to_big_camel_case, standard_str


class TablesResource(Resource):
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
