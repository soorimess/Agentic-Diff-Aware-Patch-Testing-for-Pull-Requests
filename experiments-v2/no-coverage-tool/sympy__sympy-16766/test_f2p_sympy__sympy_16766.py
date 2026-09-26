"""
Test for Indexed support in PythonCodePrinter.

This test ensures that Indexed expressions are properly converted to Python code
instead of generating warnings about unsupported expressions.
"""

from sympy import IndexedBase, pycode, Symbol


def test_indexed_single_index():
    """Test that Indexed with single index is converted properly without warnings."""
    p = IndexedBase("p")
    expr = p[0]
    result = pycode(expr)
    # Before fix: would return "# Not supported in Python:\n# Indexed\np[0]"
    # After fix: should return "p[0]" (without the warning lines)
    # Check that there are no warning lines
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    # Check that the actual code is present
    assert result.strip().endswith("p[0]")


def test_indexed_multi_index():
    """Test that Indexed with multiple indices is converted properly without warnings."""
    q = IndexedBase("q")
    expr = q[0, 1]
    result = pycode(expr)
    # Before fix: would return "# Not supported in Python:\n# Indexed\nq[0, 1]"
    # After fix: should return "q[0, 1]" (without the warning lines)
    # Check that there are no warning lines
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    # Check that the actual code is present
    assert result.strip().endswith("q[0, 1]")


def test_indexed_with_symbolic_indices():
    """Test that Indexed with symbolic indices is converted properly without warnings."""
    x = IndexedBase("x")
    i = Symbol('i')
    expr = x[i]
    result = pycode(expr)
    # Before fix: would return "# Not supported in Python:\n# Indexed\nx[i]"
    # After fix: should return "x[i]" (without the warning lines)
    # Check that there are no warning lines
    assert "# Not supported in Python:" not in result
    assert "# Indexed" not in result
    # Check that the actual code is present
    assert result.strip().endswith("x[i]")