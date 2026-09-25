"""Tests for PythonCodePrinter support of Indexed expressions."""

from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode


def test_indexed_pycode():
    """Test that Indexed expressions are properly converted to Python code."""
    # Create an Indexed expression
    p = IndexedBase("p")
    expr = p[0]
    
    # This should return the direct Python indexing syntax 
    # without the warning that it's not supported
    result = pycode(expr)
    expected = "p[0]"
    
    # Before the fix, this would have produced a warning and the string 
    # "# Not supported in Python:\n# Indexed\np[0]"
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_multidimensional_indexed_pycode():
    """Test that multidimensional Indexed expressions work properly."""
    # Create a multidimensional Indexed expression
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # This should produce the proper Python indexing syntax 
    result = pycode(expr)
    expected = "p[0, 1]"
    
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_multidimensional_three_indexed_pycode():
    """Test that three-dimensional Indexed expressions work properly."""
    # Create a 3D Indexed expression
    p = IndexedBase("p")
    expr = p[0, 1, 2]
    
    # This should produce the proper Python indexing syntax 
    result = pycode(expr)
    expected = "p[0, 1, 2]"
    
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_different_base_name_indexed_pycode():
    """Test that Indexed expressions with different base names work properly."""
    # Create Indexed expression with different base name
    q = IndexedBase("q")
    expr = q[5]
    
    # This should produce the proper Python indexing syntax 
    result = pycode(expr)
    expected = "q[5]"
    
    assert result == expected, f"Expected '{expected}', got '{result}'"