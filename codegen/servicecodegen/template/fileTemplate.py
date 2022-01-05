#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:template.py
# author:Nathan
# datetime:2021/8/26 10:59
# software: PyCharm

"""
    Template file for service layer code
"""


class FileTemplate(object):
    """
        File template class for service layer code
    """

    template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

{imports}

class {table_name_initials_upper}Service({table_name_initials_upper}Controller):
    pass
"""

    select_template = """
        # select
        @classmethod
        def select(cls, **kwargs):
            try:
                filter_List = []
                if kwargs.get('{primary_key}'):
                    filter_list.append(cls.{primary_key} == kwargs.get('{primary_key}'))
                else:
                    {get_filter_list}
               
                page = int(kwargs.get('Page',1))
                size = int(kwargs.get('Size', 10))
           
                {model_lower}_info = db.session.query(cls).filter(*filter_list)
               
                count = {model_lower}_info.count()
                pages = math.ceil(count / size)
                {model_lower}_info = {model_lower}_info.limit(size).offset((page - 1) * size).all()
       
                results = commons.query_to_dict({model_lower}_info)
                return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}}
                
            except Exception as e:
                loggings.exception(1, e)
                return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
            finally:
                db.session.close()
"""
