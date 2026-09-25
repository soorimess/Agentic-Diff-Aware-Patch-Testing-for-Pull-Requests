"""
Tests for PythonCodePrinter support of Indexed expressions.

This test ensures that the _print_Indexed method is properly implemented
in PythonCodePrinter so that Indexed expressions are printed correctly
without warnings.
"""
from sympy import IndexedBase, pycode


def test_indexed_printing():
    """Test that Indexed expressions are printed without warnings."""
    p = IndexedBase("p")
    
    # This should not produce a warning
    result = pycode(p[0])
    
    # Before the fix, this would contain warning comments
    # After the fix, this should be clean python code
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert "p[0]" == result.strip()


def test_indexed_multidimensional():
    """Test multidimensional Indexed expressions."""
    p = IndexedBase("p")
    
    # Test 2D indexing
    result = pycode(p[0, 1])
    
    # Should not contain warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    assert "p[0, 1]" == result.strip()


def test_indexed_with_expressions():
    """Test Indexed expressions with more complex indices."""
    p = IndexedBase("p")
    from sympy import Add
    
    # Test with expression indices
    result = pycode(p[Add(1, 2)])
    
    # Should not contain warning comments
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result