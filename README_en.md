##### Project Description: Python_RESTfulAPI_Codegen

This project automatically generates a complete basic API project in Python (including API documentation) based on existing database table structures. The generated project is based on the Flask+SQLAlchemy framework, and the generated APIs conform to RESTful style specifications.

The entity layer of this project is generated using the sqlalchemy-codegen tool, while the controller layer, resource layer, and service layer code are generated based on custom code templates. Basic APIs are generated automatically, and users only need to extend and add APIs related to specific business logic on this foundation.

About sqlalchemy-codegen tool:
Code repository and related links:
GitHub: https://github.com/ncepu-iDealStudio/sqlalchemy-codegen

Gitee: https://gitee.com/ncepu-bj/sqlalchemy-codegen

Documentation: https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf

PyPI: https://pypi.org/project/sqlalchemy-codegen/

##### Features of the Generated API Project:

![Screenshot](https://images.gitee.com/uploads/images/2021/0905/200245_9c40fbe9_9201274.png "Screenshot.png")

1. Layered architecture design: entity layer, service layer, controller layer, and resource layer
2. Complete basic CRUD operations: query, add, modify, delete
3. Support for logical deletion
4. Support for fuzzy queries
5. Support for pagination queries
6. Support for sorting queries
7. Support for field filtering
8. Support for field selection
9. Support for batch operations
10. Support for multi-table association queries
11. Support for custom SQL queries
12. Support for custom service methods
13. Support for custom controller methods
14. Support for custom resource methods
15. Support for custom route rules
16. Support for custom response formats
17. Support for custom error codes
18. Support for custom error messages
19. Support for custom exception handling
20. Support for custom middleware
21. Support for custom configuration
22. Support for custom logging
23. Support for custom authentication
24. Support for custom authorization
25. Support for custom validation
26. Support for custom serialization
27. Support for custom deserialization
28. Support for custom data transformation
29. Support for custom data validation
30. Support for custom data processing

##### Usage Instructions

I. Database Design Requirements

1. Each table must have a primary key field, preferably named "Id"
2. Table names should use "Pascal Case" naming convention, e.g., UserInfo
3. Table and field names cannot be Python keywords (e.g., def, False, class are incorrect)
4. Field names should use "Pascal Case" naming convention, e.g., UserName
5. It's recommended to include a timestamp field "CreateTime" defaulting to current timestamp
6. It's recommended to include a tinyint field "IsDelete" for logical deletion (0--valid, 1--deleted), defaulting to 0 (Note: this field is required if logical deletion is enabled in the generator project)

A test database script is included in the project at tests/study_api.sql; restore it to MySQL database for testing API code generation.

II. Generator Project Usage

1. Clone the repository locally:
   git clone https://gitee.com/ncepu-bj/Python_RESTfulAPI_Codegen
2. Open the project with a Python IDE (PyCharm or VSCode)
3. Configure virtual environment for the code generator project; Python version >= `3.8.0`, recommended 3.12
4. Install required packages: `pip install -r requirements.txt`
5. Run start.py in the root directory under the virtual environment, configure parameters in the UI interface
6. After execution, a dist folder will be generated containing the target project
   You can also set the target project location in the configuration file

III. Target Project Usage

1. Open the target project folder in dist using an IDE (PyCharm or VSCode)
2. Configure virtual environment for the target project; Python version >= `3.8.0`
3. Install required packages: `pip install -r requirements.txt`
