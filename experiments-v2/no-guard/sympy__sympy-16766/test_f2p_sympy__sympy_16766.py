from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing():
    """Test that Indexed expressions are printed correctly by PythonCodePrinter"""
    p = IndexedBase("p")
    expr = p[0]
    
    # This should not produce a warning about Indexed not being supported
    result = pycode(expr)
    
    # After the fix, this should produce just "p[0]" without any warning
    # Before the fix, it would produce something like:
    # "# Not supported in Python:\n# Indexed\np[0]"
    assert "# Not supported in Python:" not in result
    assert "p[0]" == result

def test_multidimensional_indexed_printing():
    """Test that multidimensional Indexed expressions are printed correctly"""
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # This should not produce a warning about Indexed not being supported
    result = pycode(expr)
    
    # After the fix, this should produce just "p[0, 1]" without any warning
    assert "# Not supported in Python:" not in result
    assert "p[0, 1]" == result

def test_indexed_with_expression_indices():
    """Test that Indexed expressions with expression indices are printed correctly"""
    from sympy import Symbol
    p = IndexedBase("p")
    i = Symbol("i")
    expr = p[i + 1]
    
    # This should not produce a warning about Indexed not being supported
    result = pycode(expr)
    
    # After the fix, this should produce just "p[i + 1]" without any warning
    assert "# Not supported in Python:" not in result
    assert "p[i + 1]" == result