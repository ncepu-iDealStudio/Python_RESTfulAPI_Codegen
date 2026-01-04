# Python_RESTfulAPI_Codegen

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0.0-brightgreen)](https://palletsprojects.com/p/flask/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-2.0.25-orange)](https://www.sqlalchemy.org/)

## 项目简介

Python_RESTfulAPI_Codegen 是一个基于数据库表结构自动生成 RESTful API 项目的代码生成器。它能够根据已有的数据库表结构，自动生成符合 RESTful 风格规范的 Python 接口项目，目标项目基于 Flask + SQLAlchemy 框架构建。

本项目旨在解决以下问题：
- 手动编写基础 CRUD 接口效率低
- 接口风格不统一
- 缺乏标准化的项目结构和文档
- 单元测试代码编写繁琐

## 核心功能

- ✅ 根据数据库表结构自动生成完整接口项目
- ✅ 生成符合 RESTful 风格的 API 接口
- ✅ 自动生成接口文档
- ✅ 自动生成单元测试代码
- ✅ 支持 Docker 容器化部署
- ✅ 支持多种数据库（MySQL、PostgreSQL、SQLite 等）

## 技术架构

### 生成器项目架构

```
Python_RESTfulAPI_Codegen/
├── app/                    # 前端界面
├── codegenerate/           # 代码生成引擎
│   ├── controllercodegen/  # 控制器层代码生成
│   ├── modelcodegen/       # 模型层代码生成
│   ├── resourcecodegen/    # 资源层代码生成
│   ├── servicecodegen/     # 服务层代码生成
│   ├── staticcodegen/      # 静态文件生成
│   ├── otherfilecodegen/   # 其他文件生成
│   └── testcodegen/        # 测试代码生成
├── config/                 # 配置文件
├── static/                 # 静态资源和部署文件
├── utils/                  # 工具类
├── tests/                  # 测试文件
├── start.py                # 项目启动入口
└── requirements.txt        # 项目依赖
```

### 生成的目标项目架构

```
generated_project/
├── app/                    # 项目初始化文件
├── config/                 # 配置文件
├── models/                 # 实体层（数据模型）
├── controller/             # 控制器层（基础操作）
├── service/                # 服务层（业务逻辑）
├── api_1_0/                # 资源层（API接口）
├── test/                   # 单元测试
├── deploy/                 # 部署配置文件
├── utils/                  # 工具类
├── manage.py               # 项目管理脚本
├── requirements.txt        # 项目依赖
├── dockerfile              # Docker 配置
└── docker-compose.yml      # Docker Compose 配置
```

## 技术栈

- **后端框架**: Flask 3.0.0 + SQLAlchemy 2.0.25
- **数据库**: 支持 MySQL、PostgreSQL、SQLite 等 SQLAlchemy 支持的数据库
- **代码生成工具**: sqlalchemy-codegen 1.1.2
- **测试框架**: pytest
- **部署**: Docker + Gunicorn + Nginx + Supervisor
- **前端**: Flask 内置模板引擎

## 安装与使用

### 环境要求

- Python 3.8+
- pip
- virtualenv
- Git

### 安装步骤

1. 克隆项目到本地：
```bash
git clone https://github.com/ncepu-iDealStudio/Python_RESTfulAPI_Codegen.git
```

2. 进入项目目录并创建虚拟环境：
```bash
cd Python_RESTfulAPI_Codegen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装项目依赖：
```bash
pip install -r requirements.txt
```

4. 启动项目：
```bash
python start.py
```

5. 在浏览器中打开 `http://127.0.0.1:5000` 进行配置和代码生成

### 使用流程

1. 准备数据库表结构（需符合设计规范）
2. 启动生成器项目并配置数据库连接参数
3. 生成目标项目代码
4. 在生成的项目中添加业务逻辑
5. 部署项目

## 数据库设计规范

为了确保代码生成器能够正确工作，请遵循以下数据库设计规范：

1. 每个表必须有主键字段，推荐命名为 "Id"
2. 表名和字段名不能使用 Python 关键字（如 def, False, class 等）
3. 表名推荐使用帕斯卡命名法（PascalCase），如 UserInfo
4. 字段名推荐使用帕斯卡命名法，如 UserName
5. 建议包含时间戳字段 "CreateTime"，默认值为当前时间
6. 建议包含 tinyint 类型的 "IsDelete" 字段用于逻辑删除（0-有效，1-已删除）

## 项目特点

### 生成的目标项目具有以下特性：

1. 分层架构设计：实体层、控制器层、资源层和服务层
2. 完整的基础 CRUD 操作：查询、新增、修改、删除
3. 支持逻辑删除
4. 支持模糊查询
5. 支持分页查询
6. 支持排序查询
7. 支持字段过滤
8. 支持字段选择
9. 支持批量操作
10. 支持多表关联查询
11. 支持自定义 SQL 查询
12. 支持 JWT 认证
13. 支持接口限流
14. 支持数据加密（AES/RSA）
15. 支持 Docker 容器化部署

## 目标项目测试

生成的目标项目内置了单元测试框架，可以方便地进行接口测试：

1. 在 `test` 目录下添加测试数据
2. 运行 `python -m pytest` 执行测试
3. 查看测试报告

## 部署

支持多种部署方式：

### Docker 部署

```bash
docker-compose up -d
```

### 传统部署

使用 Gunicorn + Nginx 部署，配置文件位于 `deploy/` 目录下。

## 相关项目

- [sqlalchemy-codegen](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen) - 本项目使用的实体层代码生成工具

## 常见问题

### ModuleNotFoundError: No module named 'flask._compat'

**解决方案**：
修改 `flask_script/__init__.py` 文件，将 `from ._compat import text_type` 改为 `from flask_script._compat import text_type`

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助我们改进项目。

## 许可证

[MIT License](LICENSE)
