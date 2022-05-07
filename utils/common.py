#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:python_sqla_codegen
# author:PigKnight
# datetime:2021/8/21 11:28
# software: PyCharm

"""
    General method
"""


# 连字符转驼峰
def str_format_convert(string):
    new_string = ''
    for word in string.split('_'):
        if new_string:
            new_string += word.lower().capitalize()
        else:
            new_string = word
    return new_string


# 字符串转全小写
def str_to_all_small(string):
    new_string = string.replace('_', '').lower()

    return new_string


# 字符串转小驼峰
def str_to_little_camel_case(string):
    new_string = ''
    for word in string.split('_'):
        if new_string:
            new_string += word[0].upper() + word[1:]
        else:
            new_string = word

    return new_string


# 字符串转大驼峰
def str_to_big_camel_case(string):
    new_string = ''
    for word in string.split('_'):
        new_string += word[0].upper() + word[1:]

    return new_string


# 字符串转全小写,单词之间-隔开
def standard_str(in_str):
    # 把字符串转换成列表
    str_list = list(in_str)
    flag = False
    for i in in_str:
        if i.isupper():
            flag = True
    # 用循环取出每一个元素
    if flag:
        for i in in_str:
            # 判断元素是否是大写
            if i.isupper():
                # 如果是大写就记录下标位置
                index = str_list.index(i)
                # 判断如果是第一个首字母则跳出本次循环
                if index == 0:
                    str_list[index] = i.lower()
                    continue
                # 修改数据，把大写转换成小写和添加-
                str_list[index] = i.lower()
                str_list.insert(index, "-")

            elif i.isalnum() is False:
                str_list[str_list.index(i)] = ''

    out_str = "".join(str_list).replace('_', '-')

    return out_str


if __name__ == '__main__':
    # ll = ['user_info', 'UserInfo', 'userinfo']
    # for l in ll:
    #     print(l, '->', str_to_little_camel_case(l))

    ss = ['LogSystemLog', 'Log_SystemLog', 'log_system_log', 'Log!System?Log']
    for s in ss:
        print(s, ' -> ', standard_str(s))
