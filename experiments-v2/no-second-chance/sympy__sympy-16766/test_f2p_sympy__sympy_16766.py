from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing():
    """Test that Indexed expressions are properly printed by PythonCodePrinter"""
    p = IndexedBase("p")
    expr = p[0]
    
    # This should not produce a warning and should return valid Python code
    result = pycode(expr)
    
    # Before the fix, this would produce a warning and return something like:
    # "# Not supported in Python:\n# Indexed\np[0]"
    # After the fix, this should return just "p[0]"
    assert result == "p[0]"

def test_multidimensional_indexed_printing():
    """Test that multi-dimensional Indexed expressions are properly printed"""
    q = IndexedBase("q")
    expr = q[0, 1]
    
    result = pycode(expr)
    
    # Should return just "q[0, 1]" without warnings
    assert result == "q[0, 1]"

def test_indexed_with_symbolic_indices():
    """Test that Indexed expressions with symbolic indices are properly printed"""
    q = IndexedBase("q")
    from sympy import Symbol
    i = Symbol('i')
    expr = q[i]
    
    result = pycode(expr)
    
    # Should return just "q[i]" without warnings
    assert result == "q[i]"