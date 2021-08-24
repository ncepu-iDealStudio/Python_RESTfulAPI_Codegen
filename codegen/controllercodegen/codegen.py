#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegen.py
# author:Itsuka
# datetime:2021/8/24 10:04
# software: PyCharm

"""
    this is function description
"""
import sys
from decimal import Decimal


type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):
    template = """\
# coding: utf-8
{imports}


class {class_name}({parent_model}):

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
            return {'code': RET.OK, 'message': '添加成功', 'data': results}
        except Exception as e:
            db.session.rollback()
            return {'code': RET.DBERR, 'message': '数据库异常，添加失败', 'error': str(e)}
        finally:
            db.session.close()
    
    # 查询
    @classmethod
    def get(cls, **kwargs)
        try:
            filter_list = []
            {get_filter_list}
            info = db.session.query(cls).filter(*filter_list).all()
            
            # 判断返回的数据是否为空
            if not info:
                return {'code': RET.NODATA, 'message': '无查询结果', 'error': '无查询结果'}
            results = commons.query_to_dict(info)
            return {'code': RET.OK, 'message': '查询成功', 'data': results}
        except Exception as e:
            return {'code': RET.DBERR, 'message': '数据库异常，查询失败', 'error': str(e)}
        finally:
            db.session.close()
    
    # 删除
    @classmethod
    def delete(cls, **kwargs):
        try:
            {delete}
            if res < 1:
                return {'code': RET.NODATA， 'message': '无可删除结果', 'error': '无可删除结果'
            db.session.commit()
            return {'code': RET.OK, 'message': '删除成功'}
        except Exception as e:
            db.session.rollback()
            return {'code': RET.DBERR, 'message': '数据库异常，删除失败', 'error': str(e)}
        finally:
            db.session.close()
    
    # 修改
    @classmethod
    def update(cls, **kwargs):
        try:
            {update}
            if res < 1:
                return {'code': RET.NODATA, 'message': '无可修改结果', 'error': '无可修改结果'}
            db.session.commit()
            return {'code': RET.OK, 'message': '修改成功'}
        except Exception as e:
            db.session.rollback()
            return {'code': RET.DBERR, 'message': '数据库异常，修改失败', 'error': str(e)}
        finally:
            db.session.close()

"""

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, outfile=sys.stdout):
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
                if j.type.python_type in type_map.keys():
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = type_map[j.type.python_type]
                else:
                    table_dict[str(i)]['columns'][str(j.name)]['type'] = 'str'

        for i in table_dict:
            imports = '''
            from app import db
            from models.{model_name} import {parent_model}
            from utils import commons
            from utils.response_code import RET
            '''

