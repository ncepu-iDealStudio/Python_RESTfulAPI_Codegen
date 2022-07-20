#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:verify_operate
# author:Nathan
# datetime:2020/10/12 13:15
# software: PyCharm

"""
   越权访问验证函数
"""

from functools import wraps

from flask import g, jsonify

from .response_code import RET, error_map_EN


# 定义一个装饰器: 用户角色验证（解决垂直越权问题：验证用户的类型是否有权操作调用接口）
def verify_user_role(role_list):
    """
    :param role_list: List[int] or Set[int] or Tuple[int] 允许访问的角色代码
    获取装饰器的传参
    """

    def _verify_userRole(func):
        """
        获取函数
        """

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            """
            获取函数传参
            """
            if g.user.get("user_type") not in role_list:
                return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "您的操作权限不足"})
            return func(*func_args, **func_kwargs)

        return wrapper

    return _verify_userRole


# 定义一个装饰器: 用户操作对象(资源)和身份是否匹配--验证操作的资源是否属于当前用户
def verify_operator_object(role_list, controller):
    """
    :param role_list: List[int] or Set[int] or Tuple[int] 允许访问的角色代码(不需要越权验证的角色)
    获取装饰器的传参
    """
    def _verify_userRole(func):
        """
        获取函数
        """

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            """
            获取函数传参
            """
            if g.user.get("user_type") not in role_list:
                res = controller.get(**func_kwargs)
                if res.get('code') == RET.OK and res.get('totalCount') > 0:
                    if g.user.get("user_id") not in list(res.get('data')[0].values()):
                        # 若数据库设计中user_id为string类型,则改为str(g.user.get("user_id"))
                        return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "您无权操作此对象"})
            return func(*func_args, **func_kwargs)

        return wrapper

    return _verify_userRole