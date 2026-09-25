# -*- coding: utf-8 -*-
"""
Regression test for Indexed printing in PythonCodePrinter
This test ensures that Indexed objects are properly printed without warnings
"""

from sympy import IndexedBase, Indexed
from sympy.printing.pycode import PythonCodePrinter


def test_indexed_printing():
    """Test that Indexed expressions are printed without warning"""
    p = IndexedBase("p")
    expr = p[0]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # Before the fix, this would return a string with warning comments
    # After the fix, this should return just "p[0]" without any warning
    assert "Not supported in Python" not in result
    assert result.strip() == "p[0]"


def test_multi_dimensional_indexed_printing():
    """Test that multi-dimensional Indexed expressions are properly printed"""
    p = IndexedBase("p")
    expr = p[0, 1, 2]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # Should return "p[0, 1, 2]" without warning 
    assert "Not supported in Python" not in result
    assert result.strip() == "p[0, 1, 2]"


def test_complex_indexed_printing():
    """Test that Indexed expressions with complex indices are properly printed"""
    from sympy import Symbol
    p = IndexedBase("p")
    i = Symbol('i')
    j = Symbol('j')
    expr = p[i, j]
    
    printer = PythonCodePrinter()
    result = printer.doprint(expr)
    
    # Should return "p[i, j]" without warning
    assert "Not supported in Python" not in result
    assert result.strip() == "p[i, j]"