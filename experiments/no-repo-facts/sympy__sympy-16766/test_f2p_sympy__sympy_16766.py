from sympy import IndexedBase, Indexed
from sympy.printing.pycode import PythonCodePrinter

def test_indexed_printing():
    """Test that PythonCodePrinter correctly handles Indexed expressions"""
    p = IndexedBase("p")
    
    # Test that indexed expressions do not generate warnings
    printer = PythonCodePrinter()
    result = printer.doprint(p[0])
    
    # Before fix, this would produce a warning with "# Not supported in Python:" 
    # After fix, this should just return "p[0]"
    
    # The test should ensure that there is no warning about unsupported features
    assert "# Not supported in Python:" not in result
    assert result == "p[0]"
    
    # Additional test for multi-dimensional indexed
    result2 = printer.doprint(p[0, 1])
    assert "# Not supported in Python:" not in result2
    assert result2 == "p[0, 1]"
    
    # Test with more complex indexing
    result3 = printer.doprint(p[0, 1, 2])
    assert "# Not supported in Python:" not in result3
    assert result3 == "p[0, 1, 2]"
    
    # Test with symbolic indices
    from sympy import symbols
    i, j = symbols('i j')
    result4 = printer.doprint(p[i, j])
    assert "# Not supported in Python:" not in result4
    assert result4 == "p[i, j]"


def test_indexed_vs_indexedbase():
    """Test the difference between Indexed and IndexedBase printing"""
    p = IndexedBase("p") 
    indexed_expr = Indexed(p, 0)
    
    printer = PythonCodePrinter()
    result = printer.doprint(indexed_expr)
    
    # Should not produce any warning 
    assert "# Not supported in Python:" not in result
    assert result == "p[0]"