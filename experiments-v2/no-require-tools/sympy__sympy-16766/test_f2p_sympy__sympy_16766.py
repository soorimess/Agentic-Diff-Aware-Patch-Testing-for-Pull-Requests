from sympy import IndexedBase, Indexed, symbols
from sympy.printing.pycode import pycode

def test_indexed_printing_single_index():
    """Test that Indexed objects with single index are printed correctly"""
    p = IndexedBase("p")
    expr = p[0]
    
    # This should work after the fix
    result = pycode(expr)
    
    # Before the fix, this would produce a warning and the raw expression
    # After the fix, this should produce valid Python code
    expected = "p[0]"
    
    # The test should pass with the fix, fail without it
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_indexed_printing_multiple_indices():
    """Test that Indexed objects with multiple indices are printed correctly"""
    p = IndexedBase("p")
    i, j = symbols('i j')
    expr = p[i, j]
    
    # This should work after the fix
    result = pycode(expr)
    
    # After the fix, this should produce valid Python code
    expected = "p[i, j]"
    
    # The test should pass with the fix, fail without it
    assert result == expected, f"Expected '{expected}', got '{result}'"