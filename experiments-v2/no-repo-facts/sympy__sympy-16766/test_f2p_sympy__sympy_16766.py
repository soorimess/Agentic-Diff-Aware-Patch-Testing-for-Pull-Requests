# -*- coding: utf-8 -*-
"""
Test for Indexed support in PythonCodePrinter
This test verifies that Indexed expressions are properly converted to Python code
without warnings, as reported in issue sympy/sympy#16766.
"""

from sympy import IndexedBase, pycode


def test_indexed_pycode():
    """Test that Indexed expressions are printed without warnings."""
    p = IndexedBase("p")
    
    # This should not produce a warning message
    result = pycode(p[0])
    
    # The result should be clean Python code without warning comments
    assert result == "p[0]", f"Expected 'p[0]', got {repr(result)}"


def test_multidimensional_indexed_pycode():
    """Test that multidimensional Indexed expressions work correctly."""
    p = IndexedBase("p")
    
    # Test 2D indexing
    result = pycode(p[0, 1])
    assert result == "p[0, 1]", f"Expected 'p[0, 1]', got {repr(result)}"
    
    # Test 3D indexing
    result = pycode(p[0, 1, 2])
    assert result == "p[0, 1, 2]", f"Expected 'p[0, 1, 2]', got {repr(result)}"


def test_indexed_with_symbols():
    """Test Indexed expressions with symbolic indices."""
    from sympy import symbols
    p = IndexedBase("p")
    i, j = symbols("i j")
    
    result = pycode(p[i, j])
    expected = "p[i, j]"
    assert result == expected, f"Expected {repr(expected)}, got {repr(result)}"