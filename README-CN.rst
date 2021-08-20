This is a tool that reads the structure of an existing database and generates the appropriate
SQLAlchemy model code, using the declarative style if possible.

这是一个根据现有的数据库结构并尽可能地使用声明风格生成适当的SQLAlchemy模版代码。

This tool was written as a replacement for `sqlautocode`_, which was suffering from several issues
(including, but not limited to, incompatibility with Python 3 and the latest SQLAlchemy version).

这个工具是作为存在一些问题(包括但不限于不限于Python3和最新的SQLAlchemy版本不兼容)的`sqlautocode`_的替代品而被编写，

.. _sqlautocode: http://code.google.com/p/sqlautocode/

Features 特性
========

* Supports SQLAlchemy 0.8.x - 1.3.x
* 支持SQLAlchemy 0.8x - 1.3x
* Produces declarative code that almost looks like it was hand written
* 生成的声明性代码几乎看起来像是手写的
* Produces `PEP 8`_ compliant code
* 生成的代码符合 `PEP 8`_规范
* Accurately determines relationships, including many-to-many, one-to-one
* 准确判断包括多对多与一对一的关系
* Automatically detects joined table inheritance
* 自动检测连接表继承
* Excellent test coverage
* 出色的测试覆盖率

.. _PEP 8: http://www.python.org/dev/peps/pep-0008/


Usage instructions 使用说明
==================

Installation 安装
------------

To install, do::

要安装，请执行::

    pip install sqlacodegen


Example usage 示例用法
-------------

At the minimum, you have to give sqlacodegen a database URL. The URL is passed directly to
SQLAlchemy's `create_engine()`_ method so please refer to `SQLAlchemy's documentation`_ for
instructions on how to construct a proper URL.

最低限度下，你必须为sqlacodegen提供一个数据库URL。URL将被直接传递给SQLAlchemy的 `create_engine()`_方法，因此请参阅`SQLAlchemy'的文档`_以获取有关如何正确构造URL的说明。

Examples::

例子::

    sqlacodegen postgresql:///some_local_db
    sqlacodegen mysql+oursql://user:password@localhost/dbname
    sqlacodegen sqlite:///database.db

To see the full list of options::

要查看选项的完整列表::

    sqlacodegen --help

.. _create_engine(): http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
.. _SQLAlchemy's documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html


Why does it sometimes generate classes and sometimes Tables? 为什么有时生成类而有时生成表?
------------------------------------------------------------

Unless the ``--noclasses`` option is used, sqlacodegen tries to generate declarative model classes
from each table. There are two circumstances in which a ``Table`` is generated instead:

除非使用了 ``--noclasses``选项，否则sqlacodegen会尝试从每个表生成声明性模型类。有两种情况会生成``表``:

* the table has no primary key constraint (which is required by SQLAlchemy for every model class)
* 该表没有主键约束(SQLAlchemy对每个模型类都需要)
* the table is an association table between two other tables (see below for the specifics)
* 该表是另外两个表之间的关联表(具体见下文)


Model class naming logic 模型类命名逻辑
------------------------

The table name (which is assumed to be in English) is converted to singular form using the
"inflect" library. Then, every underscore is removed while transforming the next letter to upper
case. For example, ``sales_invoices`` becomes ``SalesInvoice``.

表名(假定为英文)通过"inflect"库转换为单数形式。然后，删除下划线并将其下一个字母转换为大写。例如，``sales_invoices`` 转换为``SalesInvoice``。


Relationship detection logic 关系检测逻辑
----------------------------

Relationships are detected based on existing foreign key constraints as follows:

关系检测基于现有的外键约束如下:

* **many-to-one**: a foreign key constraint exists on the table
* 多对一:表上存在外键约束
* **one-to-one**: same as **many-to-one**, but a unique constraint exists on the column(s) involved
* 一对一:与多对一相同，但唯一的约束存在于涉及的列上
* **many-to-many**: an association table is found to exist between two tables
* 多对多:两个表之间存在关联表

A table is considered an association table if it satisfies all of the following conditions:

关联表如果满足以下所有条件，则将表视为关联表:

#. has exactly two foreign key constraints

#. 正好有两个外键约束

#. all its columns are involved in said constraints

#. 它的所有列都涉及到所述约束


Relationship naming logic 关系命名逻辑
-------------------------

Relationships are typically named based on the opposite class name. For example, if an ``Employee``
class has a column named ``employer`` which has a foreign key to ``Company.id``, the relationship
is named ``company``.

关系通常基于相对的类名命名。例如，如果 ``Employee``类有一个名为 ``employer`` 的列，它有一个指向``Company.id``的外键，那么这个关系就被命名为``company``。

A special case for single column many-to-one and one-to-one relationships, however, is if the
column is named like ``employer_id``. Then the relationship is named ``employer`` due to that
``_id`` suffix.

然而，单列多对一和一对一关系的一个特殊情况是，如果列的名称类似于``employer_id``，由于``_id``后缀，关系被命名为 ``employer``。

If more than one relationship would be created with the same name, the latter ones are appended
numeric suffixes, starting from 1.

如果要创建多个同名关系，则后面的关系会附加从1开始的数字后缀。


Getting help 获得帮助
============

If you have problems or other questions, you can either:

如果你有困难或者其他困惑，你可以:

* Ask on the `SQLAlchemy Google group`_, or
* 在`SQLAlchemy Google group`_上提问，或
* Ask on the ``#sqlalchemy`` channel on `Freenode IRC`_
* 在`Freenode IRC`_上的 ``#sqlalchemy``频道上提问。

.. _SQLAlchemy Google group: http://groups.google.com/group/sqlalchemy
.. _Freenode IRC: http://freenode.net/irc_servers.shtml