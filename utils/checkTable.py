#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:checkTable.py
# author:Itsuka
# datetime:2021/8/25 9:53
# software: PyCharm

"""
    检验表是否符合生成规则
"""

import keyword

from config.setting import Settings
from utils.loggings import loggings
from utils.tablesMetadata import TableMetadata


class CheckTable(object):

    # check the Primary key
    # 检查table主键
    @classmethod
    def check_primary_key(cls, table_dict):
        """
        根据代码生成模式，自动读取所有表或所需表，检验主键后返回合规的表列表
        :return: 符合规范的表名列表，即有且仅有一个自增主键，没有符合规范的情况下返回None
        """

        available_tables = []
        invalid_tables = []

        for table in table_dict.values():
            if len(table['primaryKey']) == 0:
                # 表中没有主键
                invalid_tables.append(table['table_name'])
                loggings.warning(1, 'table {0} do not have a primary key'.format(table['table_name']))
            elif len(table['primaryKey']) > 1:
                # 表中有复数个主键
                invalid_tables.append(table['table_name'])
                loggings.warning(1, 'table {0} has multiple primary keys'.format(table['table_name']))
            else:
                # 仅有一个主键，检验是否自增
                if not table['columns'][table['primaryKey'][0]]['is_autoincrement']:
                    invalid_tables.append(table['table_name'])
                    loggings.warning(1, 'table {0} do not have an autoincrement primary key'.format(table['table_name']))
                else:
                    available_tables.append(table['table_name'])

        return available_tables, invalid_tables

    # check keywords of python in tables
    # 检查表名和字段名，是否和Python的关键字冲突
    @classmethod
    def check_keyword_conflict(cls, table_dict):
        """
        check whether the table name or column name is a keyword of python
        :return: True while no table name is a keyword, else return False
        """

        available_table = []
        invalid_table = []

        for table in table_dict.values():
            flag = True

            # 检查表名是否为python关键字
            if keyword.iskeyword(table['table_name']):
                loggings.warning(1, 'table "{0}" is a keyword of python'.format(table['table_name']))
                flag = False

            for column in table['columns'].values():
                # 检查表字段是否为python关键字
                if keyword.iskeyword(column['name']):
                    loggings.warning(1, 'column "{0}.{1}" is a keyword of python'.format(table['table_name'],
                                                                                         column['name']))
                    flag = False

            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])

        return available_table, invalid_table

    # check the foreign key
    # 检查表的外键约束
    @classmethod
    def check_foreign_key(cls, table_dict):
        """
        check whether the target table of the foreign key exists
        :return: True while the target table of the foreign key exists else False
        """

        available_table = []
        invalid_table = []
        for table in table_dict.values():
            flag = True

            # 检查是否该表是否存在外键
            if not table.get('foreign_keys'):
                available_table.append(table['table_name'])
                continue
            for foreign_key in table.get('foreign_keys'):
                # 如果目标数据表不存在
                if not table_dict.get(foreign_key['target_table']):
                    loggings.warning(1, 'the target table or column "{target_table}.{target_key}" of "{source_table}.'
                                        '{source_key}" does not exist'.format(
                                         target_table=foreign_key['target_table'],
                                         target_key=foreign_key['target_key'],
                                         source_table=table['table_name'],
                                         source_key=foreign_key['key'])
                                     )
                    flag = False

            if flag:
                available_table.append(table['table_name'])
            else:
                invalid_table.append(table['table_name'])

        return available_table, invalid_table

    # 检查业务主键是否存在
    @classmethod
    def check_business_key(cls, table_dict):
        """
        检查业务主键是否存在以及是否与自增主键重复
        :return: 符合生成规则的表列表available_table和不符合生成规则的表列表invalid_table
        """

        available_table = [x['table_name'] for x in table_dict.values()]
        invalid_table = []

        # 检验业务主键字段是否存在
        for table in table_dict.values():
            if not table['business_key']:
                continue

            # 检查该业务主键是否为对应表的字段
            if table['business_key']['column'] not in table['columns'].keys():
                loggings.warning(1, 'The business key {1} of table {0} does not exist'.
                                 format(table['table_name'], table['business_key']['column']))
                invalid_table.append(available_table.pop(available_table.index(table['table_name'])))
                continue

            # 检查业务主键是否与自增主键重复
            if table['business_key']['column'] == table['primaryKey']:
                loggings.warning(1, 'The business key {1} of table {0} duplicates its auto increment primary key'.
                                 format(table['table_name'], table['business_key']['column']))
                invalid_table.append(available_table.pop(available_table.index(table['table_name'])))

        return available_table, invalid_table

    # 检验业务主键生成模板是否存在
    @classmethod
    def check_business_key_template(cls, table_dict):
        """
        检验业务主键生成模板是否存在
        :return: 符合生成规则的表列表available_table和不符合生成规则的表列表invalid_table
        """

        available_table = [x['table_name'] for x in table_dict.values()]
        invalid_table = []

        from static.utils.generate_id import GenerateID

        # 检验业务主键生成模板是否存在
        for table in table_dict.values():
            if not table['business_key']:
                continue
            if table['business_key']['rule'] == '':
                continue

            # 检查业务主键生成规则是否属于GenerateID类的属性（方法）
            if not hasattr(GenerateID, table['business_key']['rule']):
                loggings.warning(1, 'Business key generation template {} does not exist'.
                                 format(table['business_key']['rule']))
                invalid_table.append(available_table.pop(available_table.index(table['business_key']['table'])))

        return available_table, invalid_table

    # 检查要逻辑删除的表中是否存在IsDelete字段
    @classmethod
    def check_logic_delete(cls, table_dict):
        """
        检验要逻辑删除的表中是否存在IsDelete字段且数据类型为int，剔除不符合规范的表
        :return:
        """

        available_table = []
        invalid_table = []

        for table in table_dict.values():
            if not table['is_logic_delete']:
                # 采取物理删除的表
                available_table.append(str(table['table_name']))

            else:
                # 采取逻辑删除的表
                if 'IsDelete' not in [x['name'] for x in table['columns'].values()]:
                    invalid_table.append(str(table['table_name']))
                    loggings.warning(1, 'The table {} for logical deletion does not have an IsDelete field'.
                                     format(str(table['table_name'])))

                elif table['columns']['IsDelete']['type'] != 'int':
                    # IsDelete字段不为int型
                    invalid_table.append(str(table['table_name']))
                    loggings.warning(1, 'The column IsDelete of table {} is not an int type'.
                                     format(str(table['table_name'])))

                else:
                    available_table.append(str(table['table_name']))

        return available_table, invalid_table

    # 入口函数定义
    @classmethod
    def main(cls, metadata):

        # reload settings
        Settings.reload()

        table_dict = TableMetadata.get_tables_metadata(metadata)

        # check table primary key
        available_table, invalid_tables = cls.check_primary_key(table_dict)
        for invalid in invalid_tables:
            table_dict.pop(invalid)

        # check the foreign key
        available_table, invalid_table = cls.check_foreign_key(table_dict)
        invalid_tables += invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        # check the keyword
        available_table, invalid_table = cls.check_keyword_conflict(table_dict)
        invalid_tables += invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        # Check whether the business key generation template exists
        available_table, invalid_table = cls.check_business_key_template(table_dict)
        invalid_tables += invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        # check the business key
        available_table, invalid_table = cls.check_business_key(table_dict)
        invalid_tables += invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        # Check whether the IsDelete field exists in the table to be logically deleted
        available_table, invalid_table = cls.check_logic_delete(table_dict)
        available_tables = available_table
        invalid_tables += invalid_table
        for invalid in invalid_table:
            table_dict.pop(invalid)

        if len(invalid_tables) > 0:
            loggings.warning(
                1,
                "A total of {0} tables check passed.\n"
                "The following {1} tables do not meet the specifications and cannot be generated: {2}."
                    .format(
                        len(available_tables),
                        len(invalid_tables),
                        ",".join(invalid_tables)
                    )
            )

            return table_dict

        loggings.info(1, "All table checks passed, a total of {0} tables.".format(len(available_tables)))

        return table_dict
