"""
Test for the Range(range(10)) TypeError fix.

This test ensures that Range(range(10)) raises a TypeError as intended
by the pull request, rather than silently converting the range to a Range.
"""

from sympy.sets.fancysets import Range
from sympy.core.compatibility import range as py_range


def test_range_from_range_raises_typeerror():
    """Test that Range(range(10)) raises TypeError with specific message."""
    # This should raise TypeError as per the PR
    try:
        Range(py_range(10))
        # If we get here, the test failed - it should have raised
        assert False, "Range(range(10)) should raise TypeError"
    except TypeError as e:
        # Check that it has the expected error message
        assert 'use sympify' in str(e)
        assert 'to convert range to Range' in str(e)


def test_range_still_works_with_integers():
    """Test that Range still works normally with integer arguments."""
    # These should all work
    r1 = Range(10)
    assert r1 == Range(0, 10, 1)
    
    r2 = Range(5, 15)
    assert r2 == Range(5, 15, 1)
    
    r3 = Range(0, 20, 2)
    assert r3 == Range(0, 20, 2)