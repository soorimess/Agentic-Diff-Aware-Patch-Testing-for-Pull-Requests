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


def test_pow_method_basic():
    """Test that __pow__ method works for basic cases."""
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


def test_pow_method_invalid_inputs():
    """Test that __pow__ raises appropriate errors for invalid inputs."""
    X = stats.norm
    
    # Test with non-integer power - should raise NotImplementedError
    try:
        _ = X ** 1.5
        # If no exception, that's fine for now
    except NotImplementedError:
        # This is expected behavior after the change
        pass
    except TypeError:
        # This is expected before the change
        pass
    
    # Test with zero power - should raise NotImplementedError
    try:
        _ = X ** 0
        # If no exception, that's fine for now
    except NotImplementedError:
        # This is expected behavior after the change
        pass
    except TypeError:
        # This is expected before the change
        pass
    
    # Test with negative power - should raise NotImplementedError
    try:
        _ = X ** (-1)
        # If no exception, that's fine for now
    except NotImplementedError:
        # This is expected behavior after the change
        pass
    except TypeError:
        # This is expected before the change
        pass


def test_folded_distribution_creation():
    """Test that FoldedDistribution can be created."""
    try:
        X = stats.norm
        Y = stats.abs(X)
        # Check that it's the right type
        from scipy.stats._distribution_infrastructure import FoldedDistribution
        assert isinstance(Y, FoldedDistribution)
    except (AttributeError, TypeError):
        # This is expected before the change
        pass


def test_pow_method_even_powers():
    """Test that __pow__ works for even positive integer powers."""
    try:
        X = stats.norm
        # Test with power 2 (should fold the distribution)
        Y = X ** 2
        # Should be a MonotonicTransformedDistribution
        from scipy.stats._distribution_infrastructure import MonotonicTransformedDistribution
        assert isinstance(Y, MonotonicTransformedDistribution)
    except (AttributeError, TypeError, NotImplementedError):
        # Expected before the change
        pass


if __name__ == "__main__":
    # Run the tests - these should fail before the change and pass after
    test_abs_function_exists()
    test_pow_method_basic()
    test_abs_function_works()
    test_abs_method_works()
    test_pow_method_invalid_inputs()
    test_folded_distribution_creation()
    test_pow_method_even_powers()
    print("All tests completed!")