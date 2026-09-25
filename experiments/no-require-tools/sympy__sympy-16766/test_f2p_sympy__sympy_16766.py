"""
Regression tests for Indexed support in PythonCodePrinter.
This test ensures that Indexed expressions are properly converted
to Python code instead of generating warning messages.
"""

from sympy import IndexedBase, pycode


def test_indexed_printing():
    """Test that Indexed expressions are properly converted to Python code."""
    p = IndexedBase("p")
    result = pycode(p[0])
    
    # Before the fix, this returns the warning with the code
    # After the fix, this should return just the code
    expected_before_fix = '  # Not supported in Python:\n  # Indexed\np[0]'
    expected_after_fix = "p[0]"
    
    # The actual test should pass after the fix
    assert result == expected_after_fix


def test_multidimensional_indexed_printing():
    """Test that multi-dimensional Indexed expressions are properly converted."""
    p = IndexedBase("p")
    result = pycode(p[0, 1, 2])
    
    # Should return just the Python code without warnings
    expected_after_fix = "p[0, 1, 2]"
    assert result == expected_after_fix