#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    this is function description
"""
import os.path
import re

import yaml

from .read_env import read_env


def read_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value


def clear_yaml(yaml_path):
    with open(yaml_path, 'w', encoding='utf-8') as fw:
        fw.truncate()


def parse_yaml(yaml_path):
    """解析yaml文件， 实现yaml文件的参数动态化"""
    yaml_data = read_yaml(yaml_path)
    # print(yaml_data)

    # 解析config中的变量，方便下面使用
    """
        遍历测试用例的每一个步骤,解析不同参数，格式如下:
            自定义脚本:${{function_name(1,2)}}
            环境变量:${ENV(key_name)}     
            全局变量:${VAR(key_name)}       
            csv文件读取:${P(csv_file_path)} 
            变量调用:$var_name                     

    """
    variables_pattern = re.compile(r'(?<=\$)(?!\{)\w{1,}')
    env_pattern = re.compile(r'(?<=\${ENV\()\w{1,}(?=\)})')
    csv_pattern = re.compile(r'(?<=\$\{P\()\w{1,}(?=\)})')
    script_pattern = re.compile(r'(?<=\${{).*?(?=}})')

    # 获得全局环境变量的变量字典
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    env_dict = read_env(env_path)

    # 解析环境变量并进行替换
    for env_varible in env_pattern.findall(str(yaml_data)):
        pass

    # 解析变量调用并进行替换
    for var in variables_pattern.findall(str(yaml_data)):
        pass

    # 解析csv文件读取
    for path in csv_pattern.findall(str(yaml_data)):
        pass

    # 解析自定义脚本读取
    for func in script_pattern.findall(str(yaml_data)):
        pass


def func_reflect(function_name):
    import inspect
    a = inspect.getmembers(__name__)
    pass


if __name__ == '__main__':
    # parse_yaml(
    #     yaml_path=r"F:\python_file\software-test\test\test_api_1_0\studentInfoResource\login_and_get_cargoDamage.yml"
    # )
    # env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    # print(read_env(env_path))
    func_reflect(1)
