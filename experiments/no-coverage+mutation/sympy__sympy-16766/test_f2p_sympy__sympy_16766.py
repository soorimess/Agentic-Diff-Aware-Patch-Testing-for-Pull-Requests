"""
Regression tests for PythonCodePrinter not supporting Indexed expressions.

This test ensures proper handling of Indexed expressions by PythonCodePrinter.
"""

from sympy import IndexedBase, Indexed, pycode

def test_indexed_printing():
    """Test that Indexed expressions are printed correctly without warnings."""
    # Create an Indexed expression
    p = IndexedBase("p")
    expr = p[0]
    
    # Get the printed code
    result = pycode(expr)
    
    # Before the fix, this would include a warning comment
    # After the fix, it should just be the plain Python array access
    assert "# Not supported in Python:" not in result
    assert "p[0]" == result

def test_multidimensional_indexed_printing():
    """Test that multi-dimensional Indexed expressions are printed correctly."""
    # Create a multi-dimensional Indexed expression
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # Get the printed code
    result = pycode(expr)
    
    # Before the fix, this would include a warning comment  
    # After the fix, it should just be the plain Python array access
    assert "# Not supported in Python:" not in result
    assert "p[0, 1]" == result

def test_indexed_with_expression_index():
    """Test that Indexed expressions with expression indices are printed correctly."""
    from sympy import Symbol
    
    # Create an Indexed expression with symbolic index
    p = IndexedBase("p")
    i = Symbol("i")
    expr = p[i]
    
    # Get the printed code
    result = pycode(expr)
    
    # Before the fix, this would include a warning comment
    # After the fix, it should just be the plain Python array access
    assert "# Not supported in Python:" not in result
    assert "p[i]" == result