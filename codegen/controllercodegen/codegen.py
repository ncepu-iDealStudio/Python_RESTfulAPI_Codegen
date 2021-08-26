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
from decimal import Decimal

from utils.common import str_format_convert
from utils.loggings import loggings

type_map = {
    int: 'int',
    float: 'float',
    Decimal: 'float'
}


class CodeGenerator(object):
    basic_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-
{imports}


class {class_name}({parent_model}):
"""
    add_template = """
    # add
    @classmethod
    def add(cls, **kwargs):
        try:
            model = {parent_model}(
                {column_init}
            )
            db.session.add(model)
            db.session.commit()
            results = commons.query_to_dict(model)
            return {{'code': RET.OK, 'message': 'Added successfully', 'data': results}}
        except Exception as e:
            db.session.rollback()
            loggings.error(str(e))
            return {{'code': RET.DBERR, 'message': 'Database exception, failed to add', 'error': str(e)}}
        finally:
            db.session.close()
"""
    get_template = """
    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('{primary_key}'):
                filter_list.append(cls.{primary_key} == kwargs.get('{primary_key}'))
            else:
                {get_filter_list}
            info = db.session.query(cls).filter(*filter_list).all()
            
            # judge whether the data is None
            if not info:
                return {{'code': RET.NODATA, 'message': 'No query results', 'error': 'No query results'}}
            results = commons.query_to_dict(info)
            return {{'code': RET.OK, 'message': 'Queried successfully', 'data': results}}
        except Exception as e:
            loggings.error(str(e))
            return {{'code': RET.DBERR, 'message': 'Database exception, failed to query', 'error': str(e)}}
        finally:
            db.session.close()
"""
    delete_template_physical = """    
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('primary_key')
            ).with_for_update().delete()
            db.session.commit()
            return {{'code': RET.OK, 'message': 'Deleted successfully'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': 'Database exception, failed to delete', 'error': str(e)}}
        finally:
            db.session.close()
"""
    delete_template_logic = """
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('primary_key')
            ).with_for_update().update({{'IsDelete': 1}})
            if res < 1:
                return {{'code': RET.NODATA, 'message': 'No data to delete', 'error': 'No data to delete'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': 'Deleted successfully'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': 'Database exception, failed to delete', 'error': str(e)}}
        finally:
            db.session.close()
"""
    update_template = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('{primary_key}')
            ).with_for_update().update(kwargs)
            if res < 1:
                return {{'code': RET.NODATA, 'message': 'No data to update', 'error': 'No data to update'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': 'Updated successfully'}}
        except Exception as e:
            db.session.rollback()
            logggings.error(str(e))
            return {{'code': RET.DBERR, 'message': 'Database exception, failed to update', 'error': str(e)}}
        finally:
            db.session.close()
"""

    def __init__(self, metadata):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata

    def controller_codegen(self, controller_dir, delete_way='logic'):
        codes = {}
        # get table list
        table_name = self.metadata.tables.values()
        table_dict = {}
        for i in table_name:
            # get table
            table_dict[str(i)] = {}
            table_dict[str(i)]['columns'] = {}
            for j in i.c.values():
                # get column attributes
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

            # combine imports
            imports = '''
from app import db
from models.{model_name} import {parent_model}
from utils import commons
from utils.response_code import RET
from utils.loggings import loggings'''.format(model_name=model_name, parent_model=parent_model)
            basic = self.basic_template.format(imports=imports, class_name=class_name, parent_model=parent_model)

            # combine column_init
            column_init = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    continue
                else:
                    text = '''{column}=kwargs.get('{column}'),
                '''.format(column=column_k)
                    column_init += text
            add = self.add_template.format(parent_model=parent_model, column_init=column_init)

            # combine get_filter_list
            get_filter_list = ''
            for column_k, column_v in v['columns'].items():
                if column_v['autoincrement'] is True:
                    primary_key = column_k
                else:
                    if column_v['type'] in ['int', 'float']:
                        text = '''if kwargs.get('{column}') is not None:
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                '''.format(column=column_k)
                    else:
                        text = '''if kwargs.get('{column}'):
                    filter_list.append(cls.{column} == kwargs.get('{column}'))
                '''.format(column=column_k)
                    get_filter_list += text
            get = self.get_template.format(primary_key=primary_key, get_filter_list=get_filter_list)

            # combine delete
            if delete_way == 'logic':
                delete = self.delete_template_logic.format(primary_key=primary_key)
            else:
                delete = self.delete_template_physical.format(primary_key=primary_key)

            # combine update
            update = self.update_template.format(primary_key=primary_key)

            file_name = hump_str + 'Controller'
            codes[file_name] = basic + add + get + delete + update

        for k, v in codes.items():
            loggings.info(1, 'Generating {}Controller...'.format(k))
            m_file = os.path.join(controller_dir, k + '.py')
            with open(m_file, 'w', encoding='utf8') as fw:
                fw.write(v)
            loggings.info(1, '{}Controller generated successfully'.format(k))
