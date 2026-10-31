"""
Test for the Range(range(10)) behavior change.

This test ensures that Range(range(10)) raises a TypeError as intended
by the pull request, rather than silently converting the range to a Range.
"""
from sympy import Range, Symbol
from sympy.core.sympify import sympify


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


def test_range_with_symbolic_args():
    """Test that Range works with symbolic arguments properly."""
    # Test that symbolic arguments are handled correctly
    n = Symbol('n', integer=True)
    r = Range(n, n + 20, 3)
    # This should not raise an error and should have proper behavior
    assert r.start == n
    assert r.inf == n  # This should work for integer symbols


def test_range_size_with_symbolic():
    """Test that Range.size works with symbolic arguments."""
    n = Symbol('n', integer=True)
    r = Range(n, n + 10, 2)
    # This should not raise an error and should compute size properly
    size = r.size
    assert size == 5  # (n+10-n)/2 = 10/2 = 5


def test_range_iter_with_symbolic():
    """Test that Range iteration works with symbolic arguments."""
    n = Symbol('n', integer=True)
    r = Range(n, n + 5, 1)
    # This should not raise an error when accessing size for validation
    try:
        _ = r.size
        # If we get here, no error was raised
        pass
    except ValueError:
        # This would be unexpected for valid symbolic ranges
        assert False, "Should not raise ValueError for valid symbolic range"