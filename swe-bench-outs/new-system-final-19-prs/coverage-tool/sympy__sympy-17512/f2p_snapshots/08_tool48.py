"""
Test for the Range(range(10)) behavior change.

This test ensures that Range(range(10)) raises a TypeError as intended
by the pull request, rather than silently converting the range to a Range.
"""
from sympy import Range


def test_range_from_range_raises():
    """Test that Range(range(10)) raises TypeError with correct message."""
    # This should raise TypeError after the change
    # The error message should mention using sympify
    try:
        Range(range(10))
        assert False, "Expected TypeError was not raised"
    except TypeError as e:
        # This is the expected behavior after the change
        assert 'use sympify' in str(e)