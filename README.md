##### 项目说明： Python_RESTfulAPI_Codegen

能根据已有数据库表结构，自动生成Python完整的基础接口项目(包含接口的文档)；生成的目标项目基于Flask+sqlalchemy框架；所生成的接口符合restful风格规范；  

本项目实体层基于sqlalchemy-codegen工具生成，控制层和资源层以及服务层代码，基于自定义代码模板生成；基本接口已经生成，用户只需要在此基础上进行扩展增加和具体商业逻辑相关的接口即可；

关于sqlalchemy-codegen工具：
代码仓库和相关地址：
github:https://github.com/ncepu-iDealStudio/sqlalchemy-codegen

gitee:https://gitee.com/ncepu-bj/sqlalchemy-codegen

document:https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf

pypi:https://pypi.org/project/sqlalchemy-codegen/


##### 生成的目标接口项目特点：

![输入图片说明](https://images.gitee.com/uploads/images/2021/0905/200245_9c40fbe9_9201274.png "屏幕截图.png")

1. 项目架构满足分层设计规范，分为实体层，控制器层和资源层(接口层)，
   用户可以添加服务层，作为商业逻辑层；
2. 资源层(接口层)，生成了满足restful风格规范的接口，发布后，可以直接让前端调用；
   生产环境中，用户可以自行扩展接口层，对接新增加的服务层(具体商业逻辑)代码；
3. 项目定位于先有数据库表设计(数据库及表设计规范，见下面的使用说明)，后基于这些关系生成对象和实体及各层的代码；
4. 目标项目包含基于Docker容器的部署脚本；
5. 自动化生成单元测试代码；


##### 目标项目详细目录：   

└── api.sqlcodegen.com  
    ├── app  # 项目初始化文件夹  
    │   ├── __init__.py  
    │   └── setting.py  
    ├── config  # 项目配置  
    │   └── config.conf  
    ├── models # 实体层 -- 数据表对应的实体  
    │   └── userInfoModel.py  
    ├── controller  # 控制器层 -- 负责表记录的增删改查  
    │   └── userInfoController.py  
    ├── service  # 业务层 -- 负责项目主要业务逻辑的编写  
    │   └── userInfoService.py  
    ├── test # 单元测试层 -- 负责项目接口测试  
    ├── api_1_0  # 资源层 -- 负责对外暴露接口  
    │   ├── apiVersionResource  
    │   │   ├── apiVersionResource.py  
    │   │   ├── __init__.py  
    │   │   └── urls.py  
    │   └── userInfoResource  
    │       ├── __init__.py  
    │       ├── urls.py  
    │       ├── userInfoOtherResource.py  
    │       └── userInfoResource.py   
    ├── deploy  # 项目部署的配置文件  
    │   ├── gunicorn.conf  
    │   ├── nginx_flask.conf  
    │   └── supervisord.conf  
    ├── common  
    ├── docker-compose.yml  
    ├── dockerfile  
    ├── gunicorn.py  
    ├── manage.py  
    ├── requirements.txt  
    └── utils  # 常用方法工具包  
    &nbsp;&nbsp;├── commons.py  
    &nbsp;&nbsp;├── loggings.py  
    &nbsp;&nbsp;├── response_code.py  
    &nbsp;&nbsp;└── rsa_encryption_decryption.py  



##### 生成器项目的使用说明： 

更详细的帮助说明，请看帮助文档：https://idealstudio-ncepu.yuque.com/kgagg7/wdbe0k?# 《Python接口项目代码生成器使用指南》

一 数据库满足以下的设计规范（建议）  

1. 数据库表名称推荐全小写，如student；如果涉及多个描述词，可使用"_"连接。如：user_info;  
2. 数据库表的字段中，必须包含一个主键；且不能为复合主键；
3. 表的名称和表字段名称，不能是python的关键字。如：def，False, class都是不正确的  
4. 建议表的字段名称使用"大驼峰"命名法。如：UserName；  
5. 建议设计一个timestamp类型的"CreateTime"字段，默认为当前时间戳(用来记录数据创建的时间)；
6. 建议设计一个tinyint类型的"IsDelete"字段(用来实现记录的逻辑删除，0--有效，1--已删除)，默认为0（注：如果生成器项目选择使用逻辑删除，则该字段必须存在）

项目中附带了测试用数据库脚本，见tests/study_api.sql;恢复到MySQL数据库中后，即可进行接口代码生成的测试；

二 生成器项目使用

1. 先从仓库clone代码到本地;  
   git clone https://gitee.com/ncepu-bj/Python_RESTfulAPI_Codegen
2. 用Python开发工具(Pycharm或者vscode)打开项目；
3. 为代码生成器项目配置好虚拟环境；Python的版本>=`3.8.0`，推荐使用3.12
4. 安装软件运行必须的包：`pip install -r requirements.txt`
5. 在虚拟环境下，运行根目录下的start.py，在UI界面中进行相关参数的配置;
6. 程序运行完毕后，会生成dist文件夹，文件夹下即为我们需要的目标项目；
   也可以在配置文件中设置目标项目的位置；

三 目标项目测试  

1. 用开发工具（Pycharm或者vscode）打开dist中的目标项目文件夹；  

2. 为目标项目配置好虚拟环境；Python的版本>=`3.8.0`；  

3. 安装软件运行必须的包：`pip install -r requirements.txt`；  

4. 运行目标项目：`python manage.py runserver`；  

5. 打开postman进行接口测试：http://127.0.0.1:5000/api_1_0/apiversion  
   api_1_0为项目生成器中设置的版本号，如果`接口版本`参数为1.0，则此时链接中的版本号字符串为：api_1_0；  

6. 测试基本业务相关接口；  

7. 目标项目自动化测试（基于pytest）：

   打开目标项目下的test文件夹，在Test_xxxController/datas.py 及 Test_xxxResource/datas.py 中添加测试数据；

   运行test_start.py文件并生成测试报告；

四 生成器项目详细使用指南  

- <a href="https://idealstudio-ncepu.yuque.com/books/share/24f6d050-acd5-4838-a87c-6dcb3afe5e05?# 《Python代码生成器快速使用指南》" target="_blank">使用指南</a>


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

常见错误
* 1 ModuleNotFoundError: No module named 'flask._compat'
解决方法：
修改flask_script/init.py
把from ._compat import text_type 改成 from flask_script._compat import text_type
  