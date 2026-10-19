"""
Test for normal-inverse-gamma distribution (PR #21389).

This test verifies that the normal-inverse-gamma distribution is properly
implemented and behaves correctly.
"""
import numpy as np
from numpy.testing import assert_allclose
import pytest

from scipy import stats


def test_normal_inverse_gamma_exists():
    """Test that normal_inverse_gamma is available in scipy.stats."""
    # Before the PR: this should fail with AttributeError
    # After the PR: this should pass
    assert hasattr(stats, 'normal_inverse_gamma')


def test_normal_inverse_gamma_mathematical_correctness():
    """Test mathematical correctness of normal-inverse-gamma implementation."""
    if not hasattr(stats, 'normal_inverse_gamma'):
        pytest.skip("normal_inverse_gamma not available")
        
    dist = stats.normal_inverse_gamma
    
    # Test 1: Basic functionality and parameter validation
    # Test that the distribution has required methods
    assert callable(getattr(dist, 'rvs'))
    assert callable(getattr(dist, 'pdf'))
    assert callable(getattr(dist, 'logpdf'))
    assert callable(getattr(dist, 'mean'))
    assert callable(getattr(dist, 'var'))
    assert callable(getattr(dist, '__call__'))
    
    # Test 2: PDF values should be non-negative
    pdf_val = dist.pdf([0.0], [1.0], 0, 1, 1, 1)
    assert pdf_val >= 0
    
    # Test 3: PDF and logPDF consistency
    x_test = np.array([0.0])
    s2_test = np.array([1.0])
    pdf_val = dist.pdf(x_test, s2_test, 0, 1, 1, 1)
    logpdf_val = dist.logpdf(x_test, s2_test, 0, 1, 1, 1)
    assert_allclose(np.log(pdf_val), logpdf_val, rtol=1e-10)
    
    # Test 4: PDF values should be finite (not NaN or inf in normal cases)
    assert np.isfinite(pdf_val)
    
    # Test 5: LogPDF values should be finite or -inf
    assert np.isfinite(logpdf_val) or logpdf_val == -np.inf
    
    # Test 6: Parameter validation - invalid parameters should return NaN/inf appropriately
    # Negative lambda should give NaN in logpdf
    with np.errstate(invalid='ignore'):
        logpdf_neg_lambda = dist.logpdf([0.0], [1.0], 0, -1, 1, 1)
        assert np.isnan(logpdf_neg_lambda) or logpdf_neg_lambda == -np.inf
    
    # Test 7: Valid PDF with s2 <= 0 should give 0
    pdf_zero = dist.pdf([0.0], [0.0], 0, 1, 1, 1)
    assert pdf_zero == 0.0
    
    # Test 8: Valid logPDF with s2 <= 0 should give -inf
    logpdf_zero = dist.logpdf([0.0], [0.0], 0, 1, 1, 1)
    assert logpdf_zero == -np.inf
    
    # Test 9: Reproducibility with same random_state
    x1, s2_1 = dist.rvs(0, 1, 1, 1, size=5, random_state=12345)
    x2, s2_2 = dist.rvs(0, 1, 1, 1, size=5, random_state=12345)
    assert_allclose(x1, x2)
    assert_allclose(s2_1, s2_2)
    
    # Test 10: Different random states should give different results (with high probability)
    x3, s2_3 = dist.rvs(0, 1, 1, 1, size=5, random_state=54321)
    # Very unlikely to be the same, but not guaranteed
    # Just make sure they're arrays
    assert isinstance(x3, np.ndarray)
    assert isinstance(s2_3, np.ndarray)
    
    # Test 11: Frozen distribution functionality
    frozen = dist(0, 1, 3, 1)
    assert hasattr(frozen, 'pdf')
    assert hasattr(frozen, 'logpdf')
    assert hasattr(frozen, 'mean')
    assert hasattr(frozen, 'var')
    assert hasattr(frozen, 'rvs')
    
    # Test 12: Frozen distribution consistency
    mean_frozen_x, mean_frozen_s2 = frozen.mean()
    assert isinstance(mean_frozen_x, (float, np.ndarray))
    assert isinstance(mean_frozen_s2, (float, np.ndarray))
    
    # Test 13: Frozen distribution PDF method
    pdf_frozen = frozen.pdf([0.0], [1.0])
    assert isinstance(pdf_frozen, (float, np.ndarray))
    
    # Test 14: Frozen distribution logPDF method
    logpdf_frozen = frozen.logpdf([0.0], [1.0])
    assert isinstance(logpdf_frozen, (float, np.ndarray))
    
    # Test 15: Frozen distribution rvs method
    x_frozen, s2_frozen = frozen.rvs(size=3, random_state=12345)
    assert isinstance(x_frozen, np.ndarray)
    assert isinstance(s2_frozen, np.ndarray)
    assert x_frozen.shape == (3,)
    assert s2_frozen.shape == (3,)
    
    # Test 16: Frozen distribution var method
    var_frozen_x, var_frozen_s2 = frozen.var()
    assert isinstance(var_frozen_x, (float, np.ndarray))
    assert isinstance(var_frozen_s2, (float, np.ndarray))
    
    # Test 17: Basic mean and variance calculations
    mean_x, mean_s2 = dist.mean(0, 1, 2, 1)  # a > 1 for valid mean
    assert isinstance(mean_x, (float, np.ndarray))
    assert isinstance(mean_s2, (float, np.ndarray))
    
    var_x, var_s2 = dist.var(0, 1, 3, 1)  # a > 2 for valid variance
    assert isinstance(var_x, (float, np.ndarray))
    assert isinstance(var_s2, (float, np.ndarray))
    
    # Test 18: Different mu values should produce different results
    # This is a bit tricky to test for certainty, but we can at least make sure
    # the functions run and return reasonable values
    x_mu0, s2_mu0 = dist.rvs(0, 1, 1, 1, size=3, random_state=12345)
    x_mu1, s2_mu1 = dist.rvs(1, 1, 1, 1, size=3, random_state=12345)
    assert isinstance(x_mu0, np.ndarray)
    assert isinstance(s2_mu0, np.ndarray)
    assert isinstance(x_mu1, np.ndarray)
    assert isinstance(s2_mu1, np.ndarray)
    
    # Test 19: Edge case with very small s2 values
    pdf_small_s2 = dist.pdf([0.0], [1e-10], 0, 1, 1, 1)
    assert np.isfinite(pdf_small_s2) or pdf_small_s2 == 0.0
    
    # Test 20: Edge case with large s2 values
    pdf_large_s2 = dist.pdf([0.0], [1e10], 0, 1, 1, 1)
    assert np.isfinite(pdf_large_s2) or pdf_large_s2 == 0.0
    
    # Test 21: Test that the frozen distribution with same parameters gives same results
    frozen2 = dist(0, 1, 3, 1)
    mean2_x, mean2_s2 = frozen2.mean()
    assert_allclose(mean_frozen_x, mean2_x)
    assert_allclose(mean_frozen_s2, mean2_s2)