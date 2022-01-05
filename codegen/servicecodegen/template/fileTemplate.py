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

    table_template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
{imports}

class {table_name_initials_upper}Service({table_name_initials_upper}Controller):
    
    pass
"""

    view_template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
{imports}

class {table_name_initials_upper}Service(object):

    @classmethod
    def joint_query(cls, **kwargs):
    
        page = int(kwargs.get('Page', 1))
        size = int(kwargs.get('Size', 10))

        filter_list = []
    
        try:
            {table_name_lower_case}_info = db.session.query(t_{original_view_name}).filter(*filter_list)
            
            count = {table_name_lower_case}_info.count()
            pages = math.ceil(count / size)
            {table_name_lower_case}_info = {table_name_lower_case}_info.limit(size).offset((page - 1) * size).all()
            results = commons.query_to_dict({table_name_lower_case}_info)

            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}}
    
        except Exception as e:
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {{'error': str(e)}}}}
            
        finally:
            db.session.close()
"""
