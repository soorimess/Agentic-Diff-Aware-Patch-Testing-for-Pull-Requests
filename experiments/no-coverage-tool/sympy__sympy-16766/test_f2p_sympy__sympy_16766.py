"""
Regression tests for Indexed support in PythonCodePrinter

This test file verifies that the _print_Indexed method is properly
implemented in PythonCodePrinter to handle Indexed expressions
correctly.
"""

from sympy import IndexedBase, Indexed
from sympy.printing.pycode import pycode


def test_print_indexed_no_warning_comments():
    """Test that Indexed expressions don't produce warning comments."""
    p = IndexedBase("p")
    result = pycode(p[0])
    
    # Before the fix, this would include warning comments
    # After the fix, it should not contain warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result


def test_print_indexed_simple_case():
    """Test that Indexed with single index is converted to proper Python code."""
    p = IndexedBase("p")
    result = pycode(p[0])
    
    # Should contain the index access pattern
    assert "p[0]" in result
    # Should not have warning comments
    assert "# Not supported in Python:" not in result


def test_print_indexed_multi_index():
    """Test that Indexed with multiple indices is converted to proper Python code."""
    q = IndexedBase("q")
    result = pycode(q[0, 1])
    
    # Should contain the multi-index access pattern  
    assert "q[0, 1]" in result
    # Should not have warning comments
    assert "# Not supported in Python:" not in result