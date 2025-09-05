# Python_RESTfulAPI_Codegen

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0.0-brightgreen)](https://palletsprojects.com/p/flask/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-2.0.25-orange)](https://www.sqlalchemy.org/)

## Project Overview

Python_RESTfulAPI_Codegen is a code generator that automatically generates RESTful API projects based on database table structures. It can generate Python API projects that conform to RESTful style specifications based on existing database table structures. The target project is built on the Flask + SQLAlchemy framework.

This project aims to solve the following problems:
- Low efficiency in manually writing basic CRUD interfaces
- Inconsistent interface styles
- Lack of standardized project structure and documentation
- Tedious unit test code writing

## Core Features

- ✅ Automatically generate complete API projects based on database table structures
- ✅ Generate RESTful-style API interfaces
- ✅ Automatically generate API documentation
- ✅ Automatically generate unit test code
- ✅ Support Docker containerized deployment
- ✅ Support multiple databases (MySQL, PostgreSQL, SQLite, etc.)

## Technical Architecture

### Generator Project Architecture

```
Python_RESTfulAPI_Codegen/
├── app/                    # Frontend interface
├── codegenerate/           # Code generation engine
│   ├── controllercodegen/  # Controller layer code generation
│   ├── modelcodegen/       # Model layer code generation
│   ├── resourcecodegen/    # Resource layer code generation
│   ├── servicecodegen/     # Service layer code generation
│   ├── staticcodegen/      # Static file generation
│   ├── otherfilecodegen/   # Other file generation
│   └── testcodegen/        # Test code generation
├── config/                 # Configuration files
├── static/                 # Static resources and deployment files
├── utils/                  # Utility classes
├── tests/                  # Test files
├── start.py                # Project entry point
└── requirements.txt        # Project dependencies
```

### Generated Target Project Architecture

```
generated_project/
├── app/                    # Project initialization files
├── config/                 # Configuration files
├── models/                 # Entity layer (data models)
├── controller/             # Controller layer (basic operations)
├── service/                # Service layer (business logic)
├── api_1_0/                # Resource layer (API interfaces)
├── test/                   # Unit tests
├── deploy/                 # Deployment configuration files
├── utils/                  # Utility classes
├── manage.py               # Project management script
├── requirements.txt        # Project dependencies
├── dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose configuration
```

## Tech Stack

- **Backend Framework**: Flask 3.0.0 + SQLAlchemy 2.0.25
- **Database**: Supports MySQL, PostgreSQL, SQLite and other databases supported by SQLAlchemy
- **Code Generation Tool**: sqlalchemy-codegen 1.1.2
- **Testing Framework**: pytest
- **Deployment**: Docker + Gunicorn + Nginx + Supervisor
- **Frontend**: Flask built-in template engine

## Installation and Usage

### Requirements

- Python 3.8+
- pip
- virtualenv
- Git

### Installation Steps

1. Clone the project to local:
```bash
git clone https://github.com/ncepu-iDealStudio/Python_RESTfulAPI_Codegen.git
```

2. Enter the project directory and create a virtual environment:
```bash
cd Python_RESTfulAPI_Codegen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install project dependencies:
```bash
pip install -r requirements.txt
```

4. Start the project:
```bash
python start.py
```

5. Open `http://127.0.0.1:5000` in your browser to configure and generate code

### Usage Workflow

1. Prepare database table structure (must follow design specifications)
2. Start the generator project and configure database connection parameters
3. Generate target project code
4. Add business logic in the generated project
5. Deploy the project

## Database Design Specifications

To ensure the code generator works correctly, please follow these database design specifications:

1. Each table must have a primary key field, recommended to be named "Id"
2. Table names and field names cannot use Python keywords (such as def, False, class, etc.)
3. Table names are recommended to use PascalCase naming, such as UserInfo
4. Field names are recommended to use PascalCase, such as UserName
5. It is recommended to include a timestamp field "CreateTime" with the default value as the current time
6. It is recommended to include a tinyint type "IsDelete" field for logical deletion (0-valid, 1-deleted)

## Project Features

### The generated target project has the following features:

1. Layered architecture design: entity layer, controller layer, resource layer, and service layer
2. Complete basic CRUD operations: query, create, update, delete
3. Support for logical deletion
4. Support for fuzzy queries
5. Support for pagination queries
6. Support for sorting queries
7. Support for field filtering
8. Support for field selection
9. Support for batch operations
10. Support for multi-table join queries
11. Support for custom SQL queries
12. Support for JWT authentication
13. Support for API rate limiting
14. Support for data encryption (AES/RSA)
15. Support for Docker containerized deployment

## Target Project Testing

The generated target project has a built-in unit testing framework for convenient interface testing:

1. Add test data in the `test` directory
2. Run `python -m pytest` to execute tests
3. View test reports

## Deployment

Supports multiple deployment methods:

### Docker Deployment

```bash
docker-compose up -d
```

### Traditional Deployment

Deploy using Gunicorn + Nginx, configuration files are located in the `deploy/` directory.

## Related Projects

- [sqlalchemy-codegen](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen) - The entity layer code generation tool used in this project

## FAQ

### ModuleNotFoundError: No module named 'flask._compat'

**Solution**:
Modify the `flask_script/__init__.py` file, change `from ._compat import text_type` to `from flask_script._compat import text_type`

## Contributing

Issues and Pull Requests are welcome to help us improve the project.

## License

[MIT License](LICENSE)
