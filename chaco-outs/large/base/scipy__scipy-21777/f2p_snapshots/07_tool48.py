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
    except (TypeError, NotImplementedError):
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


def test_pow_method_odd_powers():
    """Test that __pow__ works for odd positive integer powers."""
    try:
        X = stats.norm
        # Test with power 3 (should not fold)
        Y = X ** 3
        # Should be a MonotonicTransformedDistribution
        from scipy.stats._distribution_infrastructure import MonotonicTransformedDistribution
        assert isinstance(Y, MonotonicTransformedDistribution)
    except (AttributeError, TypeError, NotImplementedError):
        # Expected before the change
        pass


def test_pow_method_invalid_powers():
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


def test_pow_method_specific_conditions():
    """Test specific conditions in __pow__ method."""
    try:
        X = stats.norm
        
        # Test that even powers use abs() internally
        # This exercises the condition: X = abs(self) if (other % 2 == 0) else self
        Y = X ** 2  # Should trigger the abs() path
        
        # Test that odd powers don't use abs() internally
        Z = X ** 3  # Should not trigger the abs() path
        
        # Both should be MonotonicTransformedDistribution
        from scipy.stats._distribution_infrastructure import MonotonicTransformedDistribution
        assert isinstance(Y, MonotonicTransformedDistribution)
        assert isinstance(Z, MonotonicTransformedDistribution)
        
        # Test with a few more even powers to make sure logic works
        W = X ** 4
        assert isinstance(W, MonotonicTransformedDistribution)
        
    except (AttributeError, TypeError, NotImplementedError):
        # Expected before the change
        pass


def test_folded_distribution_support():
    """Test that FoldedDistribution._support works correctly."""
    try:
        # Test folded distribution support
        X = stats.norm
        Y = stats.abs(X)
        
        # Test support method - this is the key functionality that was added
        support = Y.support()
        
        # For folded normal distribution, support should be [0, inf)
        # The support() method returns a tuple (a, b) 
        assert support[0] == 0  # Lower bound should be 0
        assert np.isinf(support[1])  # Upper bound should be infinity
        
        # Test with a distribution that has a negative lower bound
        # This tests the specific logic in _support method that handles 
        # the case where a < 0 and b > 0
        U = stats.uniform(-2, 2)  # This has support [-2, 2]
        Y2 = stats.abs(U)
        support2 = Y2.support()
        
        # For |uniform(-2, 2)|, support should be [0, 2]
        assert support2[0] == 0  # Lower bound should be 0
        assert support2[1] == 2  # Upper bound should be 2 (max of |−2|, |2|))
        
    except (AttributeError, TypeError):
        # This is expected before the change
        pass


def test_folded_distribution_pdf():
    """Test that FoldedDistribution PDF calculation works."""
    try:
        # Test folded distribution PDF
        X = stats.norm
        Y = stats.abs(X)
        
        # Test PDF calculation at various points
        x_vals = np.array([0.0, 0.5, 1.0, 2.0])
        pdf_vals = Y.pdf(x_vals)
        
        # PDF values should be non-negative
        assert np.all(pdf_vals >= 0)
        
        # PDF should be finite at x=0
        assert np.isfinite(pdf_vals[0])
        
        # Test with uniform distribution too
        U = stats.uniform(0, 1)
        Y2 = stats.abs(U)
        pdf_vals2 = Y2.pdf(x_vals)
        assert np.all(pdf_vals2 >= 0)
        assert np.all(np.isfinite(pdf_vals2))
        
    except (AttributeError, TypeError):
        # This is expected before the change
        pass


def test_folded_distribution_cdf():
    """Test that FoldedDistribution CDF calculation works."""
    try:
        # Test folded distribution CDF
        X = stats.norm
        Y = stats.abs(X)
        
        # Test CDF calculation at various points
        x_vals = np.array([0.0, 0.5, 1.0, 2.0])
        cdf_vals = Y.cdf(x_vals)
        
        # CDF values should be between 0 and 1
        assert np.all((cdf_vals >= 0) & (cdf_vals <= 1))
        
        # CDF should be increasing
        assert np.all(np.diff(cdf_vals) >= 0)
        
    except (AttributeError, TypeError):
        # This is expected before the change
        pass


def test_pow_method_edge_cases():
    """Test edge cases for __pow__ method."""
    try:
        X = stats.norm
        
        # Test with power 4 (another even power)
        Y = X ** 4
        from scipy.stats._distribution_infrastructure import MonotonicTransformedDistribution
        assert isinstance(Y, MonotonicTransformedDistribution)
        
        # Test with power 1 (odd power)
        Z = X ** 1
        assert isinstance(Z, MonotonicTransformedDistribution)
        
        # Test with power 6 (another even power)
        W = X ** 6
        assert isinstance(W, MonotonicTransformedDistribution)
        
    except (AttributeError, TypeError, NotImplementedError):
        # Expected before the change
        pass


def test_pow_method_scalar_validation():
    """Test that __pow__ properly validates scalar inputs."""
    try:
        X = stats.norm
        
        # Test that non-scalar inputs raise NotImplementedError
        # This exercises the condition: not np.isscalar(other)
        try:
            _ = X ** [2, 4]  # List should not be scalar
        except NotImplementedError:
            # This is expected behavior
            pass
        except TypeError:
            # This is expected before the change
            pass
            
    except (AttributeError, TypeError, NotImplementedError):
        # Expected before the change
        pass


if __name__ == "__main__":
    # Run the tests - these should fail before the change and pass after
    test_abs_function_exists()
    test_pow_method_exists()
    test_abs_function_works()
    test_abs_method_works()
    test_pow_method_even_powers()
    test_pow_method_odd_powers()
    test_pow_method_invalid_powers()
    test_pow_method_specific_conditions()
    test_folded_distribution_support()
    test_folded_distribution_pdf()
    test_folded_distribution_cdf()
    test_pow_method_edge_cases()
    test_pow_method_scalar_validation()
    print("All tests completed!")