##### 项目说明： Flask_Sqlachemy_RESTfulAPI_Codegen
https://github.com/ideal-ncepu/Flask_Sqlachemy_RESTfulAPI_Codegen
是一个根据数据库表结构，自动生成Python基于Flask+sqlalchemy框架的接口项目，所生成的接口符合restful风格规范；

本项目实体层基于flask-sqlacodegen工具生成，控制层和资源层以及服务层代码，基于自定义代码模板生成；

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

##### 生成器项目的使用说明： 
一 生成器项目使用
1. 先从仓库clone代码到本地；
2. 用Python开发工具(Pycharm或者vscode)打开项目；
3. 为代码生成器项目配置好虚拟环境；Pythond的版本>=3.8.0
4. 安装软件运行必须的包：pip install -r requirement.txt
5. 设置根据说明文档，好配置文件：config文件夹下的config.conf和database.conf;
6. 在虚拟环境下，运行根目录下的start.py; 
    程序运行时，会先检查各项配置文件是否有误；
7. 程序运行完毕后，会生成dist文件夹，文件夹下面及为我们需要的目标项目；   
    也可以在配置文件中设置目标项目的位置；
   
二 目标项目测试

