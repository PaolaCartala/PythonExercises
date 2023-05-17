# Python ExercisesOOP

This repository contains Python code that demonstrates the application of various concepts such as OOP, SOLID, PEP8, and other good coding practices including docstrings, linters, etc. It also incorporates the use of exceptions, decorators, unittesting, coverage.py, and logging.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Assignments](#assignments)
- [Features](#features)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Python code in this repository showcases the implementation of essential software development principles and best practices. It demonstrates the proper utilization of object-oriented programming (OOP) concepts, adhering to the SOLID principles, and following the PEP8 style guide for code formatting.

Additionally, the code includes comprehensive documentation through the use of docstrings, ensuring clarity and readability for developers. It also leverages various tools and libraries such as linters, exceptions, decorators, unittesting, coverage.py, and logging to enhance the quality, maintainability, and reliability of the codebase.

## Installation

To use the code in this repository, follow these steps:

1. Clone the repository: `git clone https://github.com/PaolaCartala/PythonExercisesOOP.git`
2. Navigate to the project directory: `cd PythonExercisesOOP`
3. Install the required dependencies: `pipenv install`

## Assignments

### Week 1
Create a set of Python functions that can be accessed from the REPL that allows to create and manage an in-memory todo list.

You need to be able to:

- Create a new empty todo list
- Add a new task to the list
- List all the current tasks
- List the task on a list
- List all todo lists
- Obtain a specific task by id
- Obtain a specific list by id
- Modify a specific task by id
- Delete a specific task
- Search for a task using its title
- Search task by contents

Also:

- Create a little terminal program which makes use of your todo list
- Use `pipenv`
- Apply PEP8
- Install `flake8`
- Manage your workflow with GitFlow

### Week 2
- Convert your first week project into an OOP project, using classes and modules.
- The project should be able to be imported to REPL or a new script, to instance new todo lists.
- The todo lists should have persistent storage in the form of text files.
- You should be able to restart the program and reload a list with the same id, and all previous tasks should be already available.
- Add the hability to add tags to the todo list tasks.
- Have in different places logic and data
- A terminal program which uses the todo list package

### Week 3
- Into the last assignment, create a suite of unittests with 80% coverage
- You might mock the file persistence

- Also:
    - Configure a `setup.py`
    - Configure the `flake8` and `coverage`
    - Have a coverage report
    - Use custom exception for validation
    - Implement `logging`

### Week 4
- Change the previous todo list module to use a `PostgreSQL` database instead of files for storage. 
- Use `SQLAlchemy` as your SQLadapter, but manage everything with raw SQL series. 
- You have to provide the tables structure for the todo list and its DDL to create the database, provide the ability to sort the tasks, group them by tag, etc. 
- Generate a SQL diagram with `Schemaspy`.
- Make sure that the test suite works for your solution and add the tests needed in order to keep the 80% + coverage.

- Extra:
    - Implement a console program which uses the todolist package
    - Include `setup.py` file
    - Log the application
    - `Schemaspy` report

## Features

- Implementation of object-oriented programming (OOP) concepts.
- Adherence to SOLID principles for enhanced software design.
- Code formatting following the PEP8 style guide.
- Comprehensive documentation through docstrings.
- Utilization of linters for code quality and style checking.
- Handling of exceptions for robust error handling.
- Implementation of decorators for modifying behavior or adding functionality.
- Unittesting using standard Python `unittest` module.
- Code coverage measurement using coverage.py.
- Logging of events, errors, and debugging information.

## Tests
The code in this repository includes a set of unit tests to ensure proper functionality and identify any regressions. To run the tests, execute the following command:

```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open a new issue or submit a pull request. Ensure that your contributions align with the existing codebase and follow the repository's coding style.

## License

This project is licensed under the [MIT License](LICENSE).
