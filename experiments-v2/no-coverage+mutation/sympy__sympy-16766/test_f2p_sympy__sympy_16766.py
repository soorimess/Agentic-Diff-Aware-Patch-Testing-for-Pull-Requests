from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode

def test_indexed_printing():
    """Test that Indexed objects are properly printed by PythonCodePrinter without warnings"""
    p = IndexedBase("p")
    expr = p[0]
    
    # This should work after the fix
    result = pycode(expr)
    
    # Before the fix, this would produce warning comments and return "p[0]"
    # After the fix, this should return "p[0]" without warnings
    # The key test is that there are no warning comments in the output
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result.strip() == "p[0]"


def test_multidimensional_indexed_printing():
    """Test that multidimensional Indexed objects are properly printed"""
    p = IndexedBase("p")
    expr = p[0, 1]
    
    # This should work after the fix
    result = pycode(expr)
    
    # The key test is that there are no warning comments in the output
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert result.strip() == "p[0, 1]"