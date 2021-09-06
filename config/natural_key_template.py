#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:natural_key_template.py
# author:Itsuka
# datetime:2021/9/5 10:08
# software: PyCharm

"""
    存放添加纪录时,业务主键生成的代码模板
"""


class NaturalKeyTemplate(object):
    """
    基本格式为：
    模板名字 = '''      import 要用到的包
        计算操作
        {natural_key} = 你的算法
'''
    自定义模板时请注意tab间隔
    本代码生成器已为您获取了m_id = 该表中的AutoID的最大值+1
    模板中的业务主键必须填{natural_key}以确保生成的代码正常运行
    自定义模板后请在本py文件的natural_key_template_dict中为其添加字典映射
    """

    # 默认模板 八位数的年月日加上四位数的AutoID
    default = """       {natural_key} = (datetime.datetime.now()).strftime('%Y%m%d') + str(m_id).zfill(4)
"""


# 业务主键生成模板的字典映射
natural_key_template_dict = {
    'default': NaturalKeyTemplate.default
}
