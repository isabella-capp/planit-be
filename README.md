
[![GitHub license](https://img.shields.io/github/license/MarinCervinschi/flask-mysql-template)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/MarinCervinschi/flask-mysql-template)]()
[![GitHub forks](https://img.shields.io/github/forks/MarinCervinschi/flask-mysql-template)]()
[![GitHub issues](https://img.shields.io/github/issues/MarinCervinschi/flask-mysql-template)]()
[![GitHub visitors](https://visitor-badge.laobi.icu/badge?page_id=MarinCervinschi.flask-mysql-template&)]()

# Flask MySQL Template 🐍🐬
## Overview

This repository provides a Flask application template integrated with MySQL. It leverages modular design principles, Docker for database containerization, and a robust testing suite to ensure ease of use and extensibility. Additionally, it uses GitHub Actions for automated testing to maintain code quality.

> **‼️ Use as a template:**
> 
> To use it as a template for your project, you can click on the "Use this template" button on the repository page. This will create a new repository with the same structure and files as this one.

### Technologies

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)](https://docs.pytest.org/en/6.2.x/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/python-app.yml)

- [Flask-MySQLdb](https://pypi.org/project/Flask-MySQLdb/): A Flask extension that provides MySQL database connectivity.
- [Coverage](https://coverage.readthedocs.io/en/6.2/): A tool for measuring code coverage of Python programs.

### Features

- [Project Structure](#repository-structure): Modular design for easy extensibility.
- [Getting Started](#getting-started): Instructions to set up and run the application.
- [Database Setup](#database-setup): Steps to initialize the MySQL database schema.
- [CRUD Operations](#crud-operations-in-db_routepy): Demonstrates CRUD operations using Flask and MySQL.
- [Running Tests and Coverage](#running-tests-and-coverage): Instructions to run tests and generate coverage reports.

## Continuous Integration with GitHub Actions

This repository is configured to automatically run tests on every commit and pull request using **GitHub Actions**. The CI pipeline ensures that new changes do not introduce errors or break existing features.

### GitHub Actions Workflow

•	**Location**: `.github/workflows/python-app.yml`

•	**Workflow Description**:

1.	Installs the application requirements.

2.	Sets up the testing environment using Python and MySQL.

3.	Runs the test suite to validate the application.

**Key Features:**

1.	**Automated Tests**:

•	Ensures all unit tests in the tests/ directory are executed on every commit.

•	Reports errors if any test fails, preventing the merge of faulty code.

2.	**Dependency Installation**:

•	Installs dependencies specified in requirements.txt to replicate the application environment.

3.	**Fast Feedback**:

•	Developers are notified of issues immediately after pushing code, enabling faster debugging and resolution.


### Repository Structure

```
├── README.md                  # Documentation for the repository
├── LICENSE                    # License information
├── app/                       # Core application logic
│   ├── __init__.py            # App initialization
│   ├── config.py              # Configuration settings
│   ├── db.py                  # Database connection logic
│   ├── factory.py             # Application factory pattern implementation
│   └── routes/                # Application routes
│       ├── __init__.py        # Routes initialization
│       ├── db_route.py        # Database-related routes (CRUD operations)
│       └── main.py            # Main application routes
├── docker-compose.yml         # Docker configuration for MySQL
├── requirements.txt           # Python dependencies
├── run.py                     # Entry point to run the Flask application
├── schema.sql                 # MySQL database schema
└── tests/                     # Testing suite
    ├── conftest.py            # Pytest fixtures and configurations
    ├── data.sql               # Sample data for tests
    ├── test_db.py             # Unit tests for `db.py`
    ├── test_db_route.py       # Unit tests for `db_route.py`
    ├── test_factory.py        # Unit tests for `factory.py`
    └── test_main.py           # Unit tests for `main.py`
```

## Getting Started

### Prerequisites

•	[Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

•	Python 3.9+ installed locally

•	MySQL client installed locally (optional for local database interactions)

### Running the Application

**With Docker and Flask**

1.	**Set up the** .env **File**:

Create a `.env` file in the root directory with the following content to configure the MySQL database for both Docker and Flask:
```bash
MYSQL_ROOT_PASSWORD=password # Change this to a secure password

#MYSQL_USER=root # You don't need for docker-compose

MYSQL_PASSWORD=password # Change this to a secure password (same as MYSQL_ROOT_PASSWORD)

MYSQL_HOST=127.0.0.1 # flask dosn't like localhost

MYSQL_PORT=3306 # default port

MYSQL_DATABASE=mysql_db # Change this to the desired database name
```

2.	**Start the MySQL Container**:

```bash
docker-compose up --build -d
```

3.	**Run Flask Locally**:

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```
```bash
python run.py
```

The application will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000/)

## Database Setup

**Schema Initialization**

With the MySQL container build, you also initialize the database schema.sql file.
If you change it, to apply the changes you can run the following command:
    
```bash
docker exec -i <mysql-container-name> mysql -u root -p <your-db-name> < schema.sql
```
Then you need to enter the password
```bash
Enter password: ...
```

To access the MySQL CLI, run the following command:

```bash
docker exec -it <mysql-container-name> mysql -u root -p <your-db-name>
```
## CRUD Operations in [db_route.py](app/routes/db_route.py)

The db_route.py implements CRUD (Create, Read, Update, Delete) operations using Flask and MySQL. It uses the [db.py](app/db.py) module that i created to interact with the database. It includes personal methods to handle the database connection, execute queries, and fetch results.

In particular:
- `get_db()` is a helper function that creates a database connection.
- `json_data()` is a helper function that converts the MySQL query results into JSON format.
- `query_db()` is a helper function that executes a query and returns the results.
    - It accepts the query and a tuple of parameters.
    - It has also two optional parameters: `one` and `commit` that are set to False by default.
        - `one` is used to fetch a single result.
            - By default, it is set to False and returns all results.
        - `commit` is used to commit the transaction.
            - It is set to True when the query is an INSERT, UPDATE, or DELETE operation.
    - It returns the query results as a list of dictionaries.
- `init_db()` is a helper function that initializes the database schema.
    - It reads the schema.sql file and executes the queries to create the tables.
    - It's a command line that you can run to initialize the database schema.
    
        ```bash
        flask init-db
        ```

These routes demonstrate how to use db.py functions to interact with the database effectively. Refer to [db_route.py](app/routes/db_route.py) for implementation details.

## Running Tests and Coverage

1.	**Run Tests**:
```bash
python -m pytest tests/
```
2.	**Run Specific Test**:

```bash
python -m pytest tests/<test_file_name>.py
```

3. Generate a coverage report:
```bash
coverage run -m pytest
coverage report
```

4. To generate an HTML coverage report:
```bash
coverage html
```
Open `htmlcov/index.html` in your web browser to view the report.

---
### Contributing

Check out the [contributing guidelines](.github/CONTRIBUTING.md) to get involved in the project.

### Issues

- Bug issues: [Report a bug](.github/ISSUE_TEMPLATE/bug_report.md)
- Custom issues: [Custom issue](.github/ISSUE_TEMPLATE/custom.md)
- Feature requests: [Request a feature](.github/ISSUE_TEMPLATE/feature_request.md)

# Happy Coding! 😊