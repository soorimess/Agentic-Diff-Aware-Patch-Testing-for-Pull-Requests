"""
Regression test for Indexed handling in PythonCodePrinter.

This test ensures that Indexed expressions are properly converted to Python code
without the "Not supported in Python" comments that would be added otherwise.
"""

from sympy import IndexedBase, pycode

def test_indexed_printing():
    """Test that Indexed expressions are printed correctly without warnings."""
    p = IndexedBase("p")
    expr = p[0]
    
    # Before the fix, this would result in:
    # "  # Not supported in Python:\n  # Indexed\np[0]" 
    # After the fix, it should be just: "p[0]"
    result = pycode(expr)
    
    # The result should not contain any "Not supported in Python" comment
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # The result should simply be p[0] (without comment lines)
    assert result.strip() == "p[0]"

def test_multidimensional_indexed_printing():
    """Test that multidimensional Indexed expressions are printed correctly."""
    p = IndexedBase("p")
    expr = p[0, 1]
    
    result = pycode(expr)
    
    # Should NOT contain unsupported comments
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should be properly formatted as p[0, 1]
    assert result.strip() == "p[0, 1]"

def test_indexed_with_variables():
    """Test Indexed with symbolic indices."""
    from sympy import symbols
    p = IndexedBase("p")
    i, j = symbols('i j')
    expr = p[i, j]
    
    result = pycode(expr)
    
    # Should NOT contain unsupported comments
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should be properly formatted with symbolic indices
    assert result.strip() == "p[i, j]"