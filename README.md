项目说明：

##### 项目名称: Python_Flask_Api_sqlalchemy_codegen；

Python_Flask_Api_sqlalchemy_codegen是一个根据数据库表结构，自动生成Python语言的
基于Flask框架+sqlalchemy框架的接口项目，所生成的接口符合restful风格规范；

##### 生成的目标接口项目特点：
1. 项目架构满足分层设计规范，分为实体层，控制器层和资源层(接口层)，
   用户可以添加服务层，作为商业逻辑层；
2. 资源层(接口层)，生成了满足restful风格规范的接口，发布后，可以直接让前端调用；
   生产环境中，用户可以自行扩展接口层，对接新增加的服务层(具体商业逻辑)代码；
3. 项目定位于先有数据库设计和关系，后基于这些关系生成对象和实体及各层的代码；

产品特性
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

##### 使用说明
安装

To install, do::

要安装，请执行::

 pip install sqlacodegen

Example usage 示例用法
-------------

最低限度下，你必须为sqlacodegen提供一个数据库URL。URL将被直接传递给SQLAlchemy的 `create_engine()`_方法，因此请参阅`SQLAlchemy'的文档`_以获取有关如何正确构造URL的说明。

Examples::

例子::

    sqlacodegen postgresql:///some_local_db
    sqlacodegen mysql+oursql://user:password@localhost/dbname
    sqlacodegen sqlite:///database.db

要查看选项的完整列表::
    sqlacodegen --help

.. _create_engine(): http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
.. _SQLAlchemy's documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html

为什么有时生成类而有时生成表?

除非使用了 ``--noclasses``选项，否则sqlacodegen会尝试从每个表生成声明性模型类。有两种情况会生成``表``:

* 该表没有主键约束(SQLAlchemy对每个模型类都需要)
* 该表是另外两个表之间的关联表(具体见下文)


模型类命名逻辑

表名(假定为英文)通过"inflect"库转换为单数形式。然后，删除下划线并将其下一个字母转换为大写。
例如，``sales_invoices`` 转换为``SalesInvoice``。


关系检测逻辑

关系检测基于现有的外键约束如下:
* **many-to-one**: a foreign key constraint exists on the table
* 多对一:表上存在外键约束
* **one-to-one**: same as **many-to-one**, but a unique constraint exists on the column(s) involved
* 一对一:与多对一相同，但唯一的约束存在于涉及的列上
* **many-to-many**: an association table is found to exist between two tables
* 多对多:两个表之间存在关联表

关联表如果满足以下所有条件，则将表视为关联表:
#. 正好有两个外键约束
#. 它的所有列都涉及到所述约束

关系命名逻辑
关系通常基于相对的类名命名。例如，如果 ``Employee``类有一个名为 ``employer`` 的列，它有一个指向``Company.id``的外键，那么这个关系就被命名为``company``。

然而，单列多对一和一对一关系的一个特殊情况是，如果列的名称类似于``employer_id``，由于``_id``后缀，关系被命名为 ``employer``。
如果要创建多个同名关系，则后面的关系会附加从1开始的数字后缀。

Getting help 获得帮助
如果你有困难或者其他困惑，你可以:
* Ask on the `SQLAlchemy Google group`_, or
* 在`SQLAlchemy Google group`_上提问，或
* Ask on the ``#sqlalchemy`` channel on `Freenode IRC`_
* 在`Freenode IRC`_上的 ``#sqlalchemy``频道上提问。

.. _SQLAlchemy Google group: http://groups.google.com/group/sqlalchemy
.. _Freenode IRC: http://freenode.net/irc_servers.shtml