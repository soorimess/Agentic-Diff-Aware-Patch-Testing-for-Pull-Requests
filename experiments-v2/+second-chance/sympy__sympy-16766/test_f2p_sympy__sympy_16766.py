from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing():
    """Test that Indexed expressions are printed correctly in Python code."""
    p = IndexedBase("p")
    expr = p[0]
    
    # Before the fix, this would produce a warning and return "p[0]"
    # After the fix, this should return "p[0]" without warnings
    result = pycode(expr)
    assert result == "p[0]"

def test_multidimensional_indexed_printing():
    """Test that multi-dimensional Indexed expressions are printed correctly."""
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # Should return "p[0, 1]" without warnings
    result = pycode(expr)
    assert result == "p[0, 1]"

def test_indexed_with_complex_indices():
    """Test that Indexed expressions with complex indices are printed correctly."""
    from sympy import symbols
    i, j = symbols('i j')
    p = IndexedBase("p")
    expr = p[i, j]
    
    # Should return "p[i, j]" without warnings
    result = pycode(expr)
    assert result == "p[i, j]"