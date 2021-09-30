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

    init_template = """\
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

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
        {business_key_init}
        try:
            model = {parent_model}(
                {column_init}
            )
            db.session.add(model)
            db.session.commit()
            results = commons.query_to_dict(model)
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    get_template = """
    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = [{get_filter_list_logic}]
            if kwargs.get('{primary_key}'):
                filter_list.append(cls.{primary_key} == kwargs.get('{primary_key}'))
            else:
                {get_filter_list}
            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            {model_lower}_info = db.session.query(cls).filter(*filter_list)
            
            count = {model_lower}_info.count()
            pages = math.ceil(count / size)
            {model_lower}_info = {model_lower}_info.limit(size).offset((page - 1) * size).all()

            # judge whether the data is None
            if not {model_lower}_info:
                return {{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No query results'}}
            results = commons.query_to_dict({model_lower}_info)
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK], 'count': count, 'pages': pages, 'data': results}}
            
        except Exception as e:
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    delete_template_physical = """    
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('{primary_key}'):
                primary_key_list = []
                for primary_key in kwargs.get('{primary_key}').replace(' ', '').split(','):
                    primary_key_list.append(cls.{primary_key} == primary_key)
                filter_list.append(or_(*primary_key_list))
            else:
                {delete_filter_list}
            res = db.session.query(cls).filter(*filter_list).with_for_update().delete()
            if res < 1:
                return {{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to delete'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK]}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    delete_template_logic = """
    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.IsDelete == 0]
            if kwargs.get('{primary_key}'):
                primary_key_list = []
                for primary_key in kwargs.get('{primary_key}').replace(' ', '').split(','):
                    primary_key_list.append(cls.{primary_key} == primary_key)
                filter_list.append(or_(*primary_key_list))
            else:
                {delete_filter_list}
            res = db.session.query(cls).filter(*filter_list).with_for_update().update({{'IsDelete': 1}})
            if res < 1:
                return {{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to delete'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK]}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    update_template_physical = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            {rsa_update}
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('{primary_key}')
            ).with_for_update().update(kwargs)
            if res < 1:
                return {{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK]}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    update_template_logic = """
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            {rsa_update}
            res = db.session.query(cls).filter(
                cls.{primary_key} == kwargs.get('{primary_key}'),
                cls.IsDelete == 0
            ).with_for_update().update(kwargs)
            if res < 1:
                return {{'code': RET.NODATA, 'message': error_map_EN[RET.NODATA], 'error': 'No data to update'}}
            db.session.commit()
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK]}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
    add_list_template = """
    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = json.loads(kwargs.get('Params'))
        model_list = []
        for param_dict in param_list:
            {add_list_business_key_init}
            model = {parent_model}(
                {add_list_column_init}
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            
            return {{'code': RET.OK, 'message': error_map_EN[RET.OK]}}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {{'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}}
        finally:
            db.session.close()
"""
