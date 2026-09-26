"""
Test for Indexed support in PythonCodePrinter.

This test ensures that PythonCodePrinter properly handles Indexed expressions
by implementing the _print_Indexed method.
"""

from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing_no_warning():
    """Test that Indexed expressions are printed without warning messages."""
    # Create an Indexed expression
    p = IndexedBase("p")
    expr = p[0]
    
    # This should not produce warning messages about unsupported features
    result = pycode(expr)
    
    # Before the fix, this would contain warning text
    # After the fix, this should only contain the Python code
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should contain the actual Python code
    assert result.strip() == "p[0]"

def test_multidimensional_indexed_printing():
    """Test that multidimensional Indexed expressions are printed without warnings."""
    # Create a multidimensional Indexed expression
    p = IndexedBase("p")
    expr = p[0, 1]
    
    result = pycode(expr)
    
    # Should not contain warning messages
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should return valid Python code
    assert result.strip() == "p[0, 1]"

def test_indexed_with_expression_index():
    """Test that Indexed expressions with expression indices are printed without warnings."""
    from sympy import symbols
    
    p = IndexedBase("p")
    i, j = symbols('i j')
    expr = p[i + j, 0]
    
    result = pycode(expr)
    
    # Should not contain warning messages
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should return valid Python code
    assert result.strip() == "p[i + j, 0]"