# Contributing to Flask MySQL Template

Thank you for considering contributing to the Flask MySQL Template! We welcome contributions to improve this project and make it even more useful for the community. Please follow the guidelines below to ensure a smooth and productive collaboration.

## Getting Started

1.	Fork the Repository:  
•	Click the “Fork” button on the top-right corner of this repository to create your own copy.  
2.	Clone the Forked Repository:
```bash
git clone https://github.com/<your-username>/flask-mysql-template.git
cd flask-mysql-template
```

3.	Set Up the Environment:
•	Install Python 3.9+ and Docker if not already installed.  
•	Install project dependencies:  
```bash
pip install -r requirements.txt
```

4.	Set Up the Database:
•	Create a `.env` file in the root directory with the necessary database configurations:  
```bash
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=flask_app
```

•	Start the MySQL container:
```bash
docker-compose up -d
```

5.	Run the Application:
```bash
python run.py
```

6.	Run the Tests:
```bash
pytest
```
## How to Contribute

### Reporting Issues

•	Search the issue tracker to check if the issue has already been reported.  
•	If not, create a new issue and provide as much detail as possible:  
•	Steps to reproduce the issue  
•	Expected and actual behavior  
•	Environment details (OS, Python version, etc.)  

### Submitting Code

1.	Create a Feature Branch:
```bash
git checkout -b feature/your-feature-name
```

2.	Write Clear, Readable Code:
•	Follow Python best practices and conventions (e.g., PEP 8).  
•	Ensure that the code is modular, documented, and includes tests.  
3.	Run Tests Locally:
•	Add or update tests for new features or fixes.  
•	Ensure all tests pass locally before submitting.  
4.	Commit Changes:
```bash
git add .
git commit -m "Add description of changes"
```

5.	Push Changes:
```bash
git push origin feature/your-feature-name
```

6.	Create a Pull Request:
•	Go to the original repository and click New Pull Request.  
•	Provide a detailed description of your changes and link any related issues.  

### Code Guidelines

1.	Follow PEP 8:  
•	Use meaningful variable names and write concise, clear code.  
2.	Keep It Modular:  
•	Split large functions into smaller, reusable functions.  
•	Group related functionality into appropriate modules.  
3.	Document Your Code:  
•	Add docstrings to functions and classes.  
•	Update relevant sections of the README or other documentation files.  
4.	Write Tests:  
•	Add unit tests for any new functionality.  
•	Ensure full test coverage for critical code paths.  

### Workflow for Maintainers

1.	Review incoming pull requests for code quality, tests, and adherence to guidelines.
2.	Suggest changes or improvements if necessary.
3.	Merge approved pull requests into the main branch.
4.	Tag and release stable updates.

### Community Guidelines

•	Be respectful and constructive in all interactions.  
•	Provide clear, actionable feedback when reviewing contributions.  
•	Respect differing opinions and approaches.

# Thank you for contributing! 🎉
