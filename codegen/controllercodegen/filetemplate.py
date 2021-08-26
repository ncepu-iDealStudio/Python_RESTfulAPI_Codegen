#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:filetemplate.py
# author:Itsuka
# datetime:2021/8/26 10:27
# software: PyCharm

"""
    provide file template here
"""


class FileTemplate(object):

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

