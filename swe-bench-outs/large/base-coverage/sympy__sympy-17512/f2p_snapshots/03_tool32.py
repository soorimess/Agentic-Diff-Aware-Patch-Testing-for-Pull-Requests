"""
Test for Range(range(10)) behavior change.

This test ensures that Range(range(10)) raises a TypeError as
implemented in the pull request, rather than being allowed.
"""

from sympy import Range, Symbol
from sympy.core.sympify import sympify

def test_range_constructor_with_range_object():
    """Test that Range(range(10)) raises TypeError"""
    # This should raise TypeError according to the PR
    try:
        r = Range(range(10))
        # If we get here, the old behavior is still active
        assert False, "Range(range(10)) should raise TypeError"
    except TypeError as e:
        assert 'use sympify' in str(e)
        return True

def test_range_conversion_with_sympify():
    """Test that sympify(range(10)) works correctly"""
    # This should work - sympifying a range should convert to Range
    r = sympify(range(10))
    assert isinstance(r, Range)
    assert r == Range(10)

def test_range_with_integer_arguments():
    """Test that normal Range construction still works"""
    # These should all work normally
    r1 = Range(10)
    r2 = Range(0, 10)
    r3 = Range(0, 10, 2)
    
    assert list(r1) == list(range(10))
    assert list(r2) == list(range(10))
    assert list(r3) == list(range(0, 10, 2))

def test_range_with_symbolic_integer_arguments():
    """Test that symbolic integer arguments work correctly"""
    # Symbolic integer arguments should work
    n = Symbol('n', integer=True)
    r = Range(n, n + 20, 3)
    assert r.start == n
    assert r.step == 3