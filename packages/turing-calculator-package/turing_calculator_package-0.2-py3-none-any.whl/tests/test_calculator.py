import pytest
from calculator.calculator import Calculator

# Basic tests for each calculator function

def test_addition():
    """
    Test the addition method of the Calculator class.
    """
    calc = Calculator()
    calc.add(5)
    assert calc.memory == 5

def test_subtraction():
    """
    Test the subtraction method of the Calculator class.
    """
    calc = Calculator()
    calc.subtract(3)
    assert calc.memory == -3

def test_multiplication():
    """
    Test the multiplication method of the Calculator class.
    """
    calc = Calculator()
    calc.multiply(2)
    assert calc.memory == 0  # 0 * 2 = 0

def test_division():
    """
    Test the division method of the Calculator class.
    """
    calc = Calculator()
    calc.add(10)
    calc.divide(2)
    assert calc.memory == 5

def test_root():
    """
    Test the root method of the Calculator class.
    """
    calc = Calculator()
    calc.add(16)
    calc.root(2)
    assert calc.memory == 4  # square root of 16 is 4

def test_reset():
    """
    Test the reset method of the Calculator class.
    """
    calc = Calculator()
    calc.add(8)
    calc.reset()
    assert calc.memory == 0
