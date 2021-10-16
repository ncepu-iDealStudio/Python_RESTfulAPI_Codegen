##### 项目说明： Flask_Sqlachemy_RESTfulAPI_Codegen
一个根据数据库表结构，自动生成Python基于Flask+sqlalchemy框架的接口项目，所生成的接口符合restful风格规范；  

本项目实体层基于flask-sqlacodegen工具生成，控制层和资源层以及服务层代码，基于自定义代码模板生成；

##### 生成的目标接口项目特点：
1. 项目架构满足分层设计规范，分为实体层，控制器层和资源层(接口层)，
   用户可以添加服务层，作为商业逻辑层；
2. 资源层(接口层)，生成了满足restful风格规范的接口，发布后，可以直接让前端调用；
   生产环境中，用户可以自行扩展接口层，对接新增加的服务层(具体商业逻辑)代码；
3. 项目定位于先有数据库设计和关系，后基于这些关系生成对象和实体及各层的代码；
3. 目标项目包含基于Docker容器的部署脚本；

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

##### 目标项目生成结构：  

![输入图片说明](https://images.gitee.com/uploads/images/2021/0905/200245_9c40fbe9_9201274.png "屏幕截图.png")  

##### 目标项目详细目录：  
.  
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
    ├── api_1_1  # 资源层 -- 负责对外暴露接口  
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
        ├── commons.py  
        ├── loggings.py  
        ├── response_code.py  
        └── rsa_encryption_decryption.py  

##### 生成器项目的使用说明：
一 生成器项目使用
1. 先从仓库clone代码到本地；
   git clone https://gitee.com/ncepu-bj/Flask_Sqlachemy_RESTfulAPI_Codegen.git
2. 用Python开发工具(Pycharm或者vscode)打开项目；
3. 为代码生成器项目配置好虚拟环境；Python的版本>=3.8.0
4. 安装软件运行必须的包：pip install -r requirement.txt
5. 配置相关参数：根据说明文档，对配置文件中的参数进行设定，主要是config文件夹下的config.conf和database.conf（请注意查看参数前的注释）;
6. 在虚拟环境下，运行根目录下的start.py;   
    程序运行时，会先检查各项配置文件是否有误；
7. 程序运行完毕后，会生成dist文件夹，文件夹下面及为我们需要的目标项目；     
    也可以在配置文件中设置目标项目的位置；

二 目标项目测试  

1. 用开发工具（Pycharm或者vscode)打开dist中的目标项目文件夹；  

2. 为目标项目配置好虚拟环境；Pythond的版本>=3.8.0；  

3. 安装软件运行必须的包：pip install -r requirement.txt；  

4. 运行目标项目：python manage.py runserver；  

5. 打开postman进行接口测试：http://127.0.0.1:5000/api_1_0/apiversion  
    api_1_0为项目生成器中设置的版本号，如果配置参数为API_VERSION=1.0，则此时链接中的版本号字符串为：api_1_0；  
    
6. 测试基本业务相关接口；

7. 目标项目自动化测试（基于pytest）：

     打开目标项目下的test文件夹，在Test_xxxController/datas.py 及 Test_xxxResource/datas.py 中添加测试数据；

     运行test_start.py文件并生成测试报告；

     

     