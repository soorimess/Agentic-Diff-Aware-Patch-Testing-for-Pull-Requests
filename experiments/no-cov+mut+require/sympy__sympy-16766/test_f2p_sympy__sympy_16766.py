"""Test that PythonCodePrinter handles Indexed objects correctly."""

from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode


def test_indexed_support():
    """Test that Indexed objects are printed without warnings."""
    p = IndexedBase("p")
    expr = p[0]
    
    # Before the fix, this would output something like:
    # "# Not supported in Python:\n# Indexed\np[0]"
    # After the fix, this should output just "p[0]"
    
    result = pycode(expr)
    
    # The result should NOT contain warning messages
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    
    # The result should be just the plain python code
    assert result == "p[0]"


def test_multidimensional_indexed():
    """Test multidimensional Indexed objects."""
    p = IndexedBase("p")
    expr = p[0, 1, 2]
    
    result = pycode(expr)
    
    # Should produce valid python code without warnings
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result == "p[0, 1, 2]"
    
    
def test_indexed_with_symbols():
    """Test Indexed with symbol indices."""
    from sympy import symbols
    p = IndexedBase("p")
    i, j = symbols('i j')
    expr = p[i, j]
    
    result = pycode(expr)
    
    # Should handle symbolic indices properly without warnings
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result == "p[i, j]"