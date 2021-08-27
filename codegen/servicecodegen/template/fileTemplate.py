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
    @classmethod
    def joint_query(cls, **kwargs):
        try:
            filter_list = []
{filter_conditions}          
            page = int(kwargs.get('Page'), 1)
            size = int(kwargs.get('Size'), 10)
            
            {result_name} = db.session.query({table_model}).filter(*filter_list){join_table_statement}
            
            count = {result_name}.count()
            pages = math.ceil(count / size)
            {result_name} = {result_name}.limit(size).offset((page - 1) * size).all()
            
        except Exception as e:
            loggings.exc(1, e)
            return {exception_return}

        if not {result_name}:
            return {notdata_return}

        # 处理返回的数据
        results = commons.query_to_dict({result_name})
        db.session.close()
        return {success_return}
   
    """
