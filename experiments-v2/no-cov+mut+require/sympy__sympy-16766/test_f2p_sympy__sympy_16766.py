"""Test for Indexed support in PythonCodePrinter"""

from sympy import IndexedBase, pycode


def test_indexed_pycode():
    """Test that Indexed expressions are properly converted to Python code"""
    p = IndexedBase("p")
    
    # This should not produce warning comments and should return proper Python code
    result = pycode(p[0])
    
    # Before the fix, this would return something like:
    # "  # Not supported in Python:\n  # Indexed\np[0]"
    # After the fix, this should return just "p[0]"
    
    # The key test is that there are no warning comments in the output
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # The result should be valid Python code for accessing the indexed element
    assert result.strip() == "p[0]"
    
    
def test_multidimensional_indexed_pycode():
    """Test that multi-dimensional Indexed expressions work correctly"""
    p = IndexedBase("p")
    
    # Test 2D indexing
    result = pycode(p[0, 1])
    
    # Should not contain warning comments
    assert "# Not supported in Python" not in result
    assert "# Indexed" not in result
    
    # Should produce proper Python indexing
    assert result.strip() == "p[0, 1]"