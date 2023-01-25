#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:codegenerator.py
# author:Itsuka
# datetime:2021/8/24 10:04
# software: PyCharm

"""
    generate controller layer code
    This generator is a very simple boilerplate for generate controller code with Flask, flask-restful,
    marshmallow, SQLAlchemy and jwt.
    It comes with basic project structure and configuration, including blueprints, application factory
    and basics unit tests.
"""

import os.path

from codegenerate.controllercodegen.template.codeblocktemplate import CodeBlockTemplate
from codegenerate.controllercodegen.template.filetemplate import FileTemplate
from utils.loggings import loggings


class CodeGenerator(object):

    def __init__(self, table_dict):
        super().__init__()
        self.table_dict = table_dict

    def controller_codegen(self, controller_dir, session_id, ip):

        try:
            codes = {}
            # get table dict
            table_dict = self.table_dict

            # generate code and save in 'codes'
            for table in [table_view for table_view in table_dict.values() if not table_view.get('is_view')]:
                little_camel_case_str = table['table_name_little_camel_case']
                big_camel_case_str = table['table_name_big_camel_case']
                # model_name = little_camel_case_str + 'Model'
                model_name = table['table_name']
                class_name = big_camel_case_str + 'Controller'
                parent_model = big_camel_case_str
                primary_key = table['primary_key_columns'][0] if len(table['primary_key_columns']) == 1 \
                    else table['primary_key_columns']
                business_key = table['business_key_column'].get('column')

                # combine imports
                imports = CodeBlockTemplate.imports.format(
                    model_name=model_name,
                    parent_model=parent_model
                )

                if table['rsa_columns']:
                    imports += '\nfrom utils.rsa_encryption_decryption import RSAEncryptionDecryption'
                if table['aes_columns']:
                    imports += '\nfrom utils.aes_encrypt_decrypt import AESEncryptDecrypt'

                basic = FileTemplate.basic_template.format(
                    imports=imports,
                    class_name=class_name,
                    parent_model=parent_model
                )
                # 添加模块
                text = ''
                column_init = ''
                business_key_init = ''
                add_result_primary_key = ''
                for column in table['columns'].values():
                    if column['name'] == primary_key and business_key != primary_key:
                        continue
                    if column['name'] == table['logical_delete_column']:
                        continue

                    if column['name'] not in (table['rsa_columns'] + table['aes_columns']):
                        # 字段不需要加密
                        if business_key != column['name']:
                            # 当前字段不是业务主键
                            text = CodeBlockTemplate.add_column_init.format(column=column['name'])
                        else:
                            # 当前字段是业务主键
                            if table['business_key_column'].get('rule'):
                                # 是业务主键且有生成规则
                                text = CodeBlockTemplate.business_key_add.format(column=column['name'])
                                business_key_init = CodeBlockTemplate.business_key_init.format(
                                    business_key=column['name'],
                                    rule=table['business_key_column']['rule']
                                )
                            else:
                                # 是业务主键但是没有生成规则
                                text = CodeBlockTemplate.add_column_init.format(column=column['name'])
                    else:
                        # 字段需要加密
                        # 可选择加密方式
                        if column['name'] in table['rsa_columns']:
                            text = CodeBlockTemplate.rsa_add.format(column=column['name'])
                        elif column['name'] in table['aes_columns']:
                            text = CodeBlockTemplate.aes_add.format(column=column['name'])

                    column_init += text

                # 拼接返回字段
                if len(table['primary_key_columns']) > 1:
                    # 属于复合主键
                    for each_primary_key in primary_key:
                        add_result_primary_key += CodeBlockTemplate.add_result_primary_key.format(
                            primary_key=each_primary_key
                        )
                else:
                    # 不属于复合主键
                    add_result_primary_key += CodeBlockTemplate.add_result_primary_key.format(
                        primary_key=business_key if business_key else primary_key
                    )

                add = FileTemplate.add_template.format(
                    business_key_init=business_key_init,
                    parent_model=parent_model,
                    column_init=column_init,
                    add_result_primary_key=add_result_primary_key
                )

                # 查询模块
                get_filter_list = ''
                for column in table['columns'].values():
                    if column['name'] == primary_key and business_key:
                        # 当前字段是主键且有业务主键，跳过
                        continue
                    elif column['name'] == business_key:
                        # 当前字段是业务主键，跳过
                        continue
                    elif column['name'] == table['logical_delete_column']:
                        # 当前字段是删除标识位，跳过
                        continue
                    else:
                        if len(table['primary_key_columns']) > 1:
                            # 属于复合主键
                            if column['type'] in ['int', 'float']:
                                # column type is a number
                                if column['name'] in table['aes_columns']:
                                    # 属于加密字段
                                    text = CodeBlockTemplate.multi_aes_get_filter_num.format(column=column['name'])
                                else:
                                    # 不属于加密字段
                                    text = CodeBlockTemplate.multi_get_filter_num.format(column=column['name'])
                            else:
                                # column type is a string
                                if column['name'] in table['aes_columns']:
                                    # 属于加密字段
                                    text = CodeBlockTemplate.multi_aes_get_filter_str.format(column=column['name'])
                                else:
                                    # 不属于加密字段
                                    text = CodeBlockTemplate.multi_get_filter_str.format(column=column['name'])

                            get_filter_list += text
                        else:
                            # 不属于复合主键
                            if column['type'] in ['int', 'float']:
                                # column type is a number
                                if column['name'] in table['aes_columns']:
                                    # 属于加密字段
                                    text = CodeBlockTemplate.aes_get_filter_num.format(column=column['name'])
                                else:
                                    # 不属于加密字段
                                    text = CodeBlockTemplate.get_filter_num.format(column=column['name'])
                            else:
                                # column type is a string
                                if column['name'] in table['aes_columns']:
                                    # 属于加密字段
                                    text = CodeBlockTemplate.aes_get_filter_str.format(column=column['name'])
                                else:
                                    # 不属于加密字段
                                    text = CodeBlockTemplate.get_filter_str.format(column=column['name'])

                            get_filter_list += text

                if len(table['primary_key_columns']) > 1:
                    # 属于复合主键
                    get = FileTemplate.get_template.format(
                        get_filter_list_logic=CodeBlockTemplate.get_filer_list_logic.format(
                            logical_delete_mark=table['logical_delete_column']
                        ) if table['logical_delete_column'] else '',
                        get_filter_list=get_filter_list,
                        model_lower=table['table_name']
                    )
                else:
                    # 不属于复合主键
                    get = FileTemplate.get_template.format(
                        get_filter_list_logic=CodeBlockTemplate.get_filer_list_logic.format(
                            logical_delete_mark=table['logical_delete_column']
                        ) if table['logical_delete_column'] else '',
                        get_filter_list=CodeBlockTemplate.single_primary_key_get_filter.format(
                            primary_key=business_key if business_key else primary_key,
                            get_filter_list=get_filter_list if get_filter_list else 'pass'
                        ),
                        model_lower=table['table_name']
                    )

                # 删除模块
                # 拼接删除方法中的filter和results
                filter_list_init = ''
                results_primary_keys = ''
                single_primary_key_result_append = ''
                if len(table['primary_key_columns']) > 1:
                    # 属于复合主键
                    for each_primary_key in primary_key:
                        filter_list_init += CodeBlockTemplate.multi_primary_key_filter.format(
                            primary_key=each_primary_key
                        )
                        results_primary_keys += CodeBlockTemplate.multi_primary_key_result.format(
                            primary_key=each_primary_key
                        )
                else:
                    # 不属于复合主键
                    filter_list_init = CodeBlockTemplate.delete_filter.format(
                        primary_key=business_key if business_key else primary_key,
                        delete_filter_list=get_filter_list if get_filter_list else 'pass'
                    )
                    results_primary_keys = CodeBlockTemplate.results_primary_keys.format(
                        primary_key=business_key if business_key else primary_key
                    )
                    single_primary_key_result_append = CodeBlockTemplate.single_primary_key_result_append.format(
                        primary_key=business_key if business_key else primary_key
                    )
                # 拼接删除方法
                if table['logical_delete_column']:
                    # 采用逻辑删除
                    delete = FileTemplate.delete_template_logic.format(
                        logical_delete_mark=table['logical_delete_column'],
                        filter_list_init=filter_list_init,
                        results_primary_keys=results_primary_keys,
                        single_primary_key_result_append=single_primary_key_result_append
                    )
                else:
                    # 采用物理删除
                    delete = FileTemplate.delete_template_physical.format(
                        filter_list_init=filter_list_init,
                        results_primary_keys=results_primary_keys,
                        single_primary_key_result_append=single_primary_key_result_append
                    )

                # 更新模块
                # 拼接更新方法中的rsa_update
                rsa_update = ''
                aes_update = ''
                if table['rsa_columns']:
                    # several columns should be encrypted
                    for rsa_column in table['rsa_columns']:
                        text = CodeBlockTemplate.rsa_update.format(column=rsa_column)
                        rsa_update += text
                if table['aes_columns']:
                    # several columns should be encrypted
                    for aes_column in table['aes_columns']:
                        text = CodeBlockTemplate.aes_update.format(column=aes_column)
                        aes_update += text

                # 拼接更新方法中的filter_list_init
                filter_list_init = ''
                results_primary_keys = ''
                if len(table['primary_key_columns']) > 1:
                    # 属于复合主键
                    for each_primary_key in primary_key:
                        filter_list_init += CodeBlockTemplate.multi_primary_key_filter.format(
                            primary_key=each_primary_key
                        )
                        results_primary_keys += CodeBlockTemplate.multi_primary_key_result.format(
                            primary_key=each_primary_key
                        )
                else:
                    # 不属于复合主键
                    # 注：更新方法较为特殊，所用的代码块模板也为复合主键用模板
                    filter_list_init += CodeBlockTemplate.multi_primary_key_filter.format(
                        primary_key=business_key if business_key else primary_key
                    )
                    results_primary_keys += CodeBlockTemplate.multi_primary_key_result.format(
                        primary_key=business_key if business_key else primary_key
                    )

                if not table['logical_delete_column']:
                    update = FileTemplate.update_template_physical.format(
                        rsa_update=rsa_update,
                        aes_update=aes_update,
                        filter_list_init=filter_list_init,
                        results_primary_keys=results_primary_keys
                    )

                else:
                    update = FileTemplate.update_template_logic.format(
                        rsa_update=rsa_update,
                        aes_update=aes_update,
                        logical_delete_mark=table['logical_delete_column'],
                        filter_list_init=filter_list_init,
                        results_primary_keys=results_primary_keys
                    )

                # 列表添加模块
                add_list_column_init = ''
                add_list_business_key_init = ''
                for column in table['columns'].values():
                    if column['name'] == primary_key and business_key != primary_key:
                        continue
                    if column['name'] == table['logical_delete_column']:
                        continue

                    if column['name'] not in (table['rsa_columns'] + table['aes_columns']):
                        # 字段不需要加密
                        if business_key != column['name']:
                            # 当前字段不是业务主键
                            text = CodeBlockTemplate.add_list_column_init.format(column=column['name'])
                        else:
                            # 当前字段是业务主键
                            if table['business_key_column'].get('rule'):
                                # 是业务主键且有生成规则
                                text = CodeBlockTemplate.business_key_add.format(column=column['name'])
                                add_list_business_key_init = CodeBlockTemplate.add_list_business_key_init.format(
                                    business_key=column['name'],
                                    rule=table['business_key_column']['rule']
                                )
                            else:
                                # 是业务主键但是没有生成规则
                                text = CodeBlockTemplate.add_list_column_init.format(column=column['name'])

                    else:
                        # 字段需要加密
                        # 可选择加密方式
                        if column['name'] in table['rsa_columns']:
                            text = CodeBlockTemplate.add_list_rsa_add.format(column=column['name'])
                        elif column['name'] in table['aes_columns']:
                            text = CodeBlockTemplate.add_list_aes_add.format(column=column['name'])

                    add_list_column_init += text

                # 拼接返回字段
                added_record_primary_keys = ''
                if len(table['primary_key_columns']) > 1:
                    # 属于复合主键
                    for each_primary_key in primary_key:
                        added_record_primary_keys += CodeBlockTemplate.multi_primary_key_add_list_result_detail_keys.format(
                            primary_key=each_primary_key
                        )
                else:
                    # 不属于复合主键
                    added_record_primary_keys += CodeBlockTemplate.multi_primary_key_add_list_result_detail_keys.format(
                        primary_key=business_key if business_key else primary_key
                    )

                add_list = FileTemplate.add_list_template.format(
                    parent_model=parent_model,
                    add_list_business_key_init=add_list_business_key_init,
                    add_list_column_init=add_list_column_init,
                    added_record_primary_keys=added_record_primary_keys
                )

                # save into 'codes'
                file_name = little_camel_case_str + 'Controller'
                codes[file_name] = basic + add + get + delete + update + add_list

            # generate files
            loggings.info(1, 'Generating __init__...', session_id, ip)
            inti_file = os.path.join(controller_dir, '__init__.py')
            with open(inti_file, 'w', encoding='utf-8') as fw:
                fw.write(FileTemplate.init_template)

            loggings.info(1, '__init__ generated successfully', session_id, ip)
            for file_name, code in codes.items():
                loggings.info(1, 'Generating {}...'.format(file_name), session_id, ip)
                m_file = os.path.join(controller_dir, file_name + '.py')
                with open(m_file, 'w', encoding='utf-8') as fw:
                    fw.write(code)
                loggings.info(1, '{} generated successfully'.format(file_name), session_id, ip)

        except Exception as e:
            loggings.exception(1, e, session_id, ip)
