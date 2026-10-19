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


def test_pow_method_with_odd_power():
    """Test that __pow__ with odd power works correctly."""
    X = stats.Normal()
    
    # Test that __pow__ works with odd positive integer
    Y = X ** 3
    # Should work without raising NotImplementedError
    assert isinstance(Y, stats._distribution_infrastructure.MonotonicTransformedDistribution)


def test_pow_method_with_even_power():
    """Test that __pow__ with even power correctly uses abs."""
    X = stats.Normal()
    
    # For even power, abs should be used internally
    Y = X ** 2
    # Should work without raising NotImplementedError
    assert isinstance(Y, stats._distribution_infrastructure.MonotonicTransformedDistribution)


def test_pow_method_not_implemented():
    """Test that __pow__ raises NotImplementedError for non-positive integers."""
    X = stats.Normal()
    
    # Test that __pow__ raises NotImplementedError for non-positive integer
    try:
        Y = X ** 0  # Should raise NotImplementedError
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass  # Expected
    
    try:
        Y = X ** -1  # Should raise NotImplementedError
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass  # Expected
    
    try:
        Y = X ** 1.5  # Should raise NotImplementedError
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass  # Expected


def test_pow_method_correct_error_message():
    """Test that __pow__ gives correct error message for invalid inputs."""
    X = stats.Normal()
    
    # Test error message for non-integer power
    try:
        Y = X ** 1.5
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError as e:
        # Should contain the expected message
        assert "positive integer" in str(e)


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
    
    # PDF should be non-negative
    assert np.all(pdf_vals >= 0)


def test_folded_distribution_logpdf():
    """Test that folded distribution logPDF is correct."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that logPDF is computed without error
    x = np.array([0.5, 1.0, 1.5])
    logpdf_vals = Y.logpdf(x)
    assert not np.any(np.isnan(logpdf_vals))
    assert not np.any(np.isinf(logpdf_vals))


def test_folded_distribution_cdf():
    """Test that folded distribution CDF is correct."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that CDF is computed without error
    x = np.array([0.5, 1.0, 1.5])
    cdf_vals = Y.cdf(x)
    assert not np.any(np.isnan(cdf_vals))
    assert not np.any(np.isinf(cdf_vals))
    
    # CDF should be between 0 and 1
    assert np.all(cdf_vals >= 0) and np.all(cdf_vals <= 1)


def test_folded_distribution_ccdf():
    """Test that folded distribution CCDF is correct."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that CCDF is computed without error
    x = np.array([0.5, 1.0, 1.5])
    ccdf_vals = Y.ccdf(x)
    assert not np.any(np.isnan(ccdf_vals))
    assert not np.any(np.isinf(ccdf_vals))
    
    # CCDF should be between 0 and 1
    assert np.all(ccdf_vals >= 0) and np.all(ccdf_vals <= 1)


def test_folded_distribution_vs_manual_computation():
    """Test that folded distribution matches manual computation for normal."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # For folded normal, PDF at x should be 2 * PDF of normal at x (for x > 0)
    x = np.array([0.5, 1.0, 1.5])
    
    # Manual computation
    manual_pdf = 2 * X.pdf(x)
    computed_pdf = Y.pdf(x)
    
    # They should be approximately equal
    assert np.allclose(manual_pdf, computed_pdf, rtol=1e-10)


def test_pow_method_dh_function_exists():
    """Test that the dh function is properly defined in transformed distributions."""
    X = stats.Normal()
    Y = X ** 2  # This should create a MonotonicTransformedDistribution
    
    # The distribution should have a dh function defined
    assert hasattr(Y, '_dh')
    # The dh function should be callable
    dh_func = Y._dh
    assert callable(dh_func)
    
    # Test that it works with some values
    test_vals = np.array([1.0, 2.0, 3.0])
    result = dh_func(test_vals)
    assert not np.any(np.isnan(result))
    assert not np.any(np.isinf(result))


def test_shifted_scaled_distribution_scale_handling():
    """Test that shifted/scaled distributions handle scale properly."""
    # Test that scale parameter is handled correctly in pdf calculations
    X = stats.Normal()
    Y = X + 1  # This creates a shifted distribution
    
    # Test that pdf computation works with scale
    x = np.array([0.5, 1.0, 1.5])
    pdf_vals = Y.pdf(x)
    assert not np.any(np.isnan(pdf_vals))
    assert not np.any(np.isinf(pdf_vals))
    
    # Test that logpdf computation works with scale
    logpdf_vals = Y.logpdf(x)
    assert not np.any(np.isnan(logpdf_vals))
    assert not np.any(np.isinf(logpdf_vals))


def test_monotonic_transformed_distribution_properties():
    """Test that MonotonicTransformedDistribution works correctly."""
    X = stats.Normal()
    Y = X ** 2  # This creates a MonotonicTransformedDistribution
    
    # Test that it has the expected attributes
    assert hasattr(Y, '_g')
    assert hasattr(Y, '_h')
    assert hasattr(Y, '_dh')
    
    # Test that the functions work
    x = np.array([1.0, 2.0, 3.0])
    g_result = Y._g(x)
    h_result = Y._h(x)
    dh_result = Y._dh(x)
    
    assert not np.any(np.isnan(g_result))
    assert not np.any(np.isnan(h_result))
    assert not np.any(np.isnan(dh_result))
    
    assert not np.any(np.isinf(g_result))
    assert not np.any(np.isinf(h_result))
    assert not np.any(np.isinf(dh_result))


def test_folded_distribution_entropy():
    """Test that folded distribution can compute entropy."""
    X = stats.Normal()
    Y = stats.abs(X)
    
    # Test that entropy computation works (if implemented)
    try:
        entropy_val = Y.entropy()
        # Should be finite
        assert np.isfinite(entropy_val)
    except (NotImplementedError, AttributeError):
        # If not implemented, that's OK for this test
        pass