from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing_without_warnings():
    """Test that Indexed expressions are properly printed by PythonCodePrinter without warnings"""
    # Create an Indexed expression like p[0]
    p = IndexedBase("p")
    expr = p[0]
    
    # This should return clean Python code without warnings
    result = pycode(expr)
    
    # Before the fix, this would contain warning comments
    # After the fix, this should return clean Python code
    # The warning text should not be present
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result.strip() == "p[0]"

def test_multidimensional_indexed_printing_without_warnings():
    """Test that multidimensional Indexed expressions are properly printed without warnings"""
    # Create a 2D Indexed expression like p[0, 1]
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # This should return clean Python code without warnings
    result = pycode(expr)
    
    # The warning text should not be present
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result.strip() == "p[0, 1]"