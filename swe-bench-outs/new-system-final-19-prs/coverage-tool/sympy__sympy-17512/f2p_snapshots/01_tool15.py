"""
Test for the Range(range(10)) behavior change.

This test ensures that Range(range(10)) raises a TypeError as intended
by the pull request, rather than silently converting the range to a Range.
"""
from sympy import Range


def test_range_from_range_raises():
    """Test that Range(range(10)) raises TypeError."""
    # This should raise TypeError after the change
    try:
        r = Range(range(10))
        # If we get here without exception, the behavior hasn't changed
        assert False, "Expected TypeError was not raised"
    except TypeError as e:
        # This is the expected behavior after the change
        assert 'use sympify' in str(e)


def test_range_from_range_directly():
    """Test that Range(range(10)) raises TypeError directly."""
    # Before the change this worked, after the change it should raise TypeError
    try:
        Range(range(10))
        # If we get here, the old behavior still exists
        assert False, "Expected TypeError for Range(range(10))"
    except TypeError:
        # This is the new correct behavior
        pass