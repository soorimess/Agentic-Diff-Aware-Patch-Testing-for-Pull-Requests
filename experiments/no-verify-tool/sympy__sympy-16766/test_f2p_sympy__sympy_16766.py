from sympy import IndexedBase
from sympy.printing.pycode import PythonCodePrinter

def test_indexed_printing_no_warnings():
    """Test that Indexed expressions are printed without warnings by PythonCodePrinter
    
    Before the fix, this would produce:
        "# Not supported in Python:\n# Indexed\np[0]"
    
    After the fix, this should produce:
        "p[0]"
    """
    p = IndexedBase("p")
    expr = p[0]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # The fix should eliminate the warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    
    # The clean Python code representation
    assert result.strip() == "p[0]"

def test_indexed_multidim_printing_no_warnings():
    """Test that multidimensional Indexed expressions are printed without warnings"""
    p = IndexedBase("p")
    expr = p[0, 1, 2]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # The fix should eliminate the warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    
    # The clean Python code representation
    assert result.strip() == "p[0, 1, 2]"

def test_indexed_with_complex_indices():
    """Test that Indexed expressions with complex index expressions work correctly"""
    p = IndexedBase("p")
    # Using expressions as indices
    expr = p[0 + 1, 2*3]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # The fix should eliminate the warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    
    # The clean Python code representation
    assert result.strip() == "p[0 + 1, 2*3]"