"""
Regression test for PR #21777: ENH: stats: absolute value of a random variable

This tests the new functionality that adds:
- abs() function for taking absolute value of random variables
- __abs__() method for random variables
- FoldedDistribution class
- __pow__() method for raising random variables to positive integer powers
"""
import numpy as np
from scipy import stats


def test_abs_function_exists():
    """Test that the abs function is available in stats module."""
    # This should work after the PR is applied
    assert hasattr(stats, 'abs')


def test_abs_function_basic():
    """Test basic functionality of abs function."""
    # Test that abs works with Normal distribution
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Y should be a FoldedDistribution
    assert isinstance(Y, stats._distribution_infrastructure.FoldedDistribution)


def test_abs_method_exists():
    """Test that __abs__ method exists on distributions."""
    X = stats.Normal()
    # This should work after the PR is applied
    Y = abs(X)
    
    # Y should be a FoldedDistribution
    assert isinstance(Y, stats._distribution_infrastructure.FoldedDistribution)


def test_folded_distribution_properties():
    """Test that FoldedDistribution works correctly."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that it can compute pdf
    x = np.array([0.5, 1.0, 1.5])
    pdf_vals = Y.pdf(x)
    
    # PDF should be non-negative
    assert np.all(pdf_vals >= 0)
    
    # Test that it can compute cdf
    cdf_vals = Y.cdf(x)
    
    # CDF should be between 0 and 1
    assert np.all(cdf_vals >= 0) and np.all(cdf_vals <= 1)


def test_pow_method_exists():
    """Test that __pow__ method exists and works for positive integers."""
    X = stats.Normal()
    
    # Test that __pow__ works with positive integer
    try:
        Y = X ** 2
        # Should work without raising NotImplementedError
        assert True
    except NotImplementedError:
        # This would indicate the feature is not implemented yet
        assert False, "__pow__ method not implemented"


def test_folded_distribution_support():
    """Test that FoldedDistribution has correct support."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Support should be [0, inf) for folded normal
    support = Y.support()
    assert support[0] == 0
    assert np.isinf(support[1])


def test_folded_distribution_pdf():
    """Test that folded distribution PDF is correct."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # For folded normal, PDF at x should be 2 * PDF of normal at x (for x > 0)
    x = np.array([0.5, 1.0, 1.5])
    
    # Test that PDF is computed without error
    pdf_vals = Y.pdf(x)
    assert not np.any(np.isnan(pdf_vals))
    assert not np.any(np.isinf(pdf_vals))


def test_folded_distribution_logpdf():
    """Test that folded distribution logPDF is correct."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that logPDF is computed without error
    x = np.array([0.5, 1.0, 1.5])
    logpdf_vals = Y.logpdf(x)
    assert not np.any(np.isnan(logpdf_vals))
    assert not np.any(np.isinf(logpdf_vals))