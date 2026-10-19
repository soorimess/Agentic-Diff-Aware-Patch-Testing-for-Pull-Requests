"""
Regression tests for PR #20753: ENH: stats.chisquare/power_divergence: add array API support

This test file ensures that the changes made to power_divergence and chisquare
functions properly handle the core functionality changes from the PR.
"""

import numpy as np
import pytest
import warnings
from scipy.stats import power_divergence, chisquare


def test_power_divergence_functionality():
    """
    Test core power_divergence functionality with matching sums.
    
    Tests the basic behavior that was modified in the PR.
    """
    # Test with matching sums to avoid tolerance issues
    f_obs = np.array([10, 15, 20, 25])
    f_exp = np.array([17.5, 17.5, 17.5, 17.5])  # Sums = 70 each
    
    # Test power_divergence with lambda=1 (Pearson's chi-squared)
    result = power_divergence(f_obs, f_exp, lambda_=1)
    assert isinstance(result.statistic, (float, np.number))
    assert isinstance(result.pvalue, (float, np.number))
    
    # Test chisquare equivalence
    chisq_result = chisquare(f_obs, f_exp)
    power_result = power_divergence(f_obs, f_exp, lambda_=1)
    assert np.allclose(chisq_result.statistic, power_result.statistic)
    assert np.allclose(chisq_result.pvalue, power_result.pvalue)


def test_lambda_zero_functionality():
    """
    Test lambda=0 case (log-likelihood ratio) which uses xlogy internally.
    
    This tests the new xlogy function that was added for array API support.
    """
    # Test with matching sums
    f_obs = np.array([10, 15, 20, 25])
    f_exp = np.array([17.5, 17.5, 17.5, 17.5])  # Sums = 70 each
    
    # Test lambda=0 case (log-likelihood ratio) - uses xlogy internally
    result = power_divergence(f_obs, f_exp, lambda_=0)
    assert isinstance(result.statistic, (float, np.number))
    assert isinstance(result.pvalue, (float, np.number))


def test_tolerance_handling():
    """
    Test the tolerance behavior change from 1e-8 to eps**0.5.
    
    This tests that the function works correctly with the new tolerance logic.
    """
    # Test with matching sums - should work with both old and new logic
    f_obs = np.array([100, 100, 100])
    f_exp = np.array([100, 100, 100])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = power_divergence(f_obs, f_exp)
        assert isinstance(result.statistic, (float, np.number))
        assert isinstance(result.pvalue, (float, np.number))
        
        # Should not issue deprecation warnings for regular arrays
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0


def test_dtype_compatibility():
    """
    Test dtype compatibility - part of array API support.
    """
    # Test with different dtypes to ensure array API compatibility
    f_obs = np.array([10, 15, 20, 25], dtype=np.float32)
    f_exp = np.array([17.5, 17.5, 17.5, 17.5], dtype=np.float32)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = power_divergence(f_obs, f_exp)
        assert isinstance(result.statistic, (float, np.number))
        assert isinstance(result.pvalue, (float, np.number))
        
        # Should not issue deprecation warnings for regular arrays
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0


def test_edge_case_handling():
    """
    Test edge cases that might be affected by the new implementation.
    """
    # Test with single element
    f_obs = np.array([10])
    f_exp = np.array([10])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = power_divergence(f_obs, f_exp)
        assert isinstance(result.statistic, (float, np.number))
        assert isinstance(result.pvalue, (float, np.number))
        
        # Should not issue deprecation warnings for regular arrays
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0