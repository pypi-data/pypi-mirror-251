# Calculator Package for Turning Sprint 1

This Python package provides a simple calculator with basic mathematical operations as per the sprint one assingment. Following requirments has been implemented in the code.

# Objectives for this Part
 - Practice writing clean OOP-based Python code and testing it.
 - Practice creating your own Python package.
 - Understand and apply the required software license for your package.
 - Practice dealing with Python environments.

# Requirements
The main package file should contain a class Calculator that should be able to perform these actions:

- Addition / Subtraction.
- Multiplication / Division.
- Take (n) root of a number.
- Reset memory (Calculator must have its own memory, meaning it should manipulate its starting number 0 until it is reset.).

# Package Structure
utahir-DWWP.1.5/
| -- calculator/
|   | -- __init__.py
|   | -- calculator.py
| -- tests/
|   | -- __init__.py
|   | -- test_calculator.py
| -- README.md
| -- LICENSE.txt
| -- setup.py
| -- requirements.txt
| -- mypy.ini

# Calculator Project
In calculator forlder there is a calculator class with follwoing funcntions

- __init__ : as Constructer that initialized memory with value of 0 and type float.

- add(value: float) : add function takes single argument floating type value that can be integrer also and restuns the same value as defualt value is 0 if any other function is expected to be called before that value will be remail in mamory.

- subtract (value: float) : subtract take single argument restricted to float and int type value and return the value of resvced value - value_in_memory

- multiply(value: float) : multiply function takes single argument and return the recived value multiplied by value_in_memory

- divide(value: float) : divide also take single argument that must be float or int but it should not be zero as if zero provided it will rais error "cannot divide by zero.

- takeroot(nth: float) : takes the nth root of the calcluator memory and only takes single argument as nth value of type float

- rest_memory() : function takes no argument and clears the memory created by add() function.

# Tests are writen for the follwoing out puts

- test_addition() : add 5 in value funciton must return 5 and save in memory as assert will be checked on memory 

- test_subtraction() : class has been initialized again to rest memeory to zero and test run with argument value 3 the expected restult must -3 as memory value is 0 by defult

- test_multiplication() :  class for multiplication also inialized again to check the functionality as memory will be zero again and argument provided as value 2 and 2 * 0 must be zero in return. Remember here the argument check is applied not to be zero but memory by defult as per requirment is zero.

- test_divition() : method add and divid called with value of 10 and 2 and expected value in memory must return 5

- test_root() : In test root add and root methods of class calculator has been called with value of 16 for add where it replaced the any value in memory and take the root of 2 and expected value is 4

- test_rest() :  is to check if we are able to resut the memeory successfully where returned value must be zero.




# Installation

Install the package using pip:

```bash
pip install turing-calculator-package
