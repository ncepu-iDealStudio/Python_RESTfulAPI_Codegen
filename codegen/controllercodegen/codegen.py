#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegen.py
# author:Itsuka
# datetime:2021/8/24 10:04
# software: PyCharm

"""
    this is function description
"""
import os.path
import sys
from decimal import Decimal
from utils.common import str_format_convert


type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):
    basic_template = """\
# coding: utf-8
{imports}


class {class_name}({parent_model}):
"""
    add_template = """
    # 添加
    @classmethod
    def add(cls, **kwargs)
        try:
            model = {parent_model}(
                {column_init}
            )
            db.session.add(model)
            db.session.commit()
            results = commons.query_to_dict(other)
            return {{'code': RET.OK, 'message': '添加成功', 'data': results}}
        except Exception as e:
            db.session.rollback()
            loggings.error(str(e))
            return {{'code': RET.DBERR, 'message': '数据库异常，添加失败', 'error': str(e)}}
        finally:
            db.session.close()
            
"""
    get_template = """
    # 查询
    @classmethod
    def get(cls, **kwargs)
        try:
            filter_list = []
            if kwargs.get({primary_key}):
                filter_list.append(cls.{primary_key} == kwargs.get({primary_key}))
            else:
                {get_filter_list}
            info = db.session.query(cls).filter(*filter_list).all()
            
            # 判断返回的数据是否为空
            if not info:
                return {{'code': RET.NODATA, 'message': '无查询结果', 'error': '无查询结果'}}
            results = commons.query_to_dict(info)
            return {{'code': RET.OK, 'message': '查询成功', 'data': results}}
        except Exception as e:
        loggings.error(str(e))
            return {{'code': RET.DBERR, 'message': '数据库异常，查询失败', 'error': str(e)}}
        finally:
            db.session.close()

"""
    delete_template_logic = """    
    # 删除
    @classmethod
    def delete(cls, **kwargs):
        try:
            db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('primary_key')
            ).with_for_update().delete()
            db.session.commit()
            return {{'code': RET.OK, 'message': '删除成功'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': '数据库异常，删除失败', 'error': str(e)}}
        finally:
            db.session.close()
    
"""
    delete_template_physical = """
    # 删除
    @classmethod
    def delete(cls, **kwargs):
        try:
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('primary_key')
            ).with_for_update().update({{'IsDelete': 1}})
            if res < 1:
                return {{'code': RET.NODATA， 'message': '无可删除结果', 'error': '无可删除结果'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': '删除成功'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': '数据库异常，删除失败', 'error': str(e)}}
        finally:
            db.session.close()
"""
    update_template = """
    # 修改
    @classmethod
    def update(cls, **kwargs):
        try:
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('{primary_key}')
            ).with_for_update().update(kwargs)
            if res < 1:
                return {{'code': RET.NODATA, 'message': '无可修改结果', 'error': '无可修改结果'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': '修改成功'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': '数据库异常，修改失败', 'error': str(e)}}
        finally:
            db.session.close()

"""

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, controller_dir, delete_way='logic'):
        codes = {}
        # 获取表列表
        table_name = self.metadata.tables.values()
        table_dict = {}
        for i in table_name:
            # 获取表
            table_dict[str(i)] = {}
            table_dict[str(i)]['columns'] = {}
            for j in i.c.values():
                # 获得字段属性
                table_dict[str(i)]['columns'][str(j.name)] = {}
                table_dict[str(i)]['columns'][str(j.name)]['name'] = j.name
                table_dict[str(i)]['columns'][str(j.name)]['primary_key'] = j.primary_key
                table_dict[str(i)]['columns'][str(j.name)]['autoincrement'] = j.autoincrement
                if j.type.python_type in type_map.keys():
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type]
                else:
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = 'str'

        for k, v in table_dict.items():
            hump_str = str_format_convert(k)
            model_name = hump_str + 'Model'
            class_name = hump_str[0].upper() + hump_str[1:] + 'Controller'
            parent_model = hump_str[0].upper() + hump_str[1:] + 'Model'

            # 组合imports
            imports = '''
from app import db
from models.{model_name} import {parent_model}
from utils import commons
from utils.response_code import RET
from utils.loggings import loggings
'''.format(model_name=model_name, parent_model=parent_model)
            basic = self.basic_template.format(imports=imports, class_name=class_name, parent_model=parent_model)

            # 组合column_init
            column_init = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    continue
                else:
                    text = '''{column}=kwargs.get('{column}')
                '''.format(column=column_k)
                    column_init += text
            add = self.add_template.format(parent_model=parent_model, column_init=column_init)

            # 组合get_filter_list
            get_filter_list = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    primary_key = column_k
                else:
                    if column_v['type'] in ['int', 'float']:
                        text = '''if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == kwargs.get('{column}')
                '''.format(column=column_k)
                    else:
                        text = '''if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == kwargs.get('{column}')
                '''.format(column=column_k)
                    get_filter_list += text
            get = self.get_template.format(primary_key=primary_key, get_filter_list=get_filter_list)

            # 组合delete
            if delete_way == 'logic':
                delete = self.delete_template_logic.format(primary_key=primary_key)
            else:
                delete = self.delete_template_physical.format(primary_key=primary_key)

            # 组合update
            update = self.update_template.format(primary_key=primary_key)

            file_name = hump_str + 'Controller.py'
            codes[file_name] = basic + add + get + delete + update

        for k, v in codes.items():
            m_file = os.path.join(controller_dir, k)
            with open(m_file, 'w') as fw:
                fw.write(v)
