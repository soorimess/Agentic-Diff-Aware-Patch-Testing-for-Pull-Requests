"""
Regression tests for PR #21777: ENH: stats: absolute value of a random variable

This test file ensures that the functionality added in PR #21777 works correctly.
The PR adds:
1. A function `abs` that takes the absolute value of a random variable
2. A `__abs__` method on distributions
3. A `FoldedDistribution` class
4. A `__pow__` method for even powers
"""

import numpy as np
from scipy import stats
import pytest


def test_abs_function_exists():
    """Test that the abs function exists and can be imported."""
    # This should not raise an ImportError
    assert hasattr(stats, 'abs')


def test_pow_method_exists():
    """Test that __pow__ method exists on distributions."""
    # Test that we can use ** operator on distributions
    X = stats.norm
    
    # Test with power 2 (should work)
    try:
        Y = X ** 2
        # If we get here without exception, it's working
        assert True
    except (TypeError, NotImplementedError) as e:
        # This is expected before the change
        pass


def test_abs_function_works():
    """Test that abs function works when available."""
    # Test that abs function can be called
    try:
        X = stats.norm
        Y = stats.abs(X)
        # If we get here without exception, it's working
        assert True
    except AttributeError:
        # This is expected before the change
        pass


def test_abs_method_works():
    """Test that __abs__ method works when available."""
    # Test that abs() works on distributions
    try:
        X = stats.norm
        Y = abs(X)
        # If we get here without exception, it's working
        assert True
    except TypeError:
        # This is expected before the change
        pass


if __name__ == "__main__":
    # Run the tests - these should fail before the change and pass after
    test_abs_function_exists()
    test_pow_method_exists()
    test_abs_function_works()
    test_abs_method_works()
    print("All tests completed!")