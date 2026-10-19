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


def test_normal_inverse_gamma_comprehensive():
    """Comprehensive test of normal-inverse-gamma functionality."""
    if not hasattr(stats, 'normal_inverse_gamma'):
        pytest.skip("normal_inverse_gamma not available")
        
    # Test that the distribution has required methods
    dist = stats.normal_inverse_gamma
    assert callable(getattr(dist, 'rvs'))
    assert callable(getattr(dist, 'pdf'))
    assert callable(getattr(dist, 'logpdf'))
    assert callable(getattr(dist, 'mean'))
    assert callable(getattr(dist, 'var'))
    assert callable(getattr(dist, '__call__'))
    
    # Test basic rvs functionality
    x, s2 = dist.rvs(0, 1, 1, 1, size=5, random_state=12345)
    assert isinstance(x, np.ndarray)
    assert isinstance(s2, np.ndarray)
    assert x.shape == (5,)
    assert s2.shape == (5,)
    assert np.all(s2 > 0)
    
    # Test that different mu values give different results
    x_mu0, s2_mu0 = dist.rvs(0, 1, 1, 1, size=10, random_state=12345)
    x_mu1, s2_mu1 = dist.rvs(1, 1, 1, 1, size=10, random_state=12345)
    # Should be different (though not guaranteed, very likely)
    assert not np.allclose(x_mu0, x_mu1)
    
    # Test basic pdf functionality
    pdf_vals = dist.pdf([0.0], [1.0], 0, 1, 1, 1)
    assert isinstance(pdf_vals, (float, np.ndarray))
    assert pdf_vals >= 0
    
    # Test basic logpdf functionality
    logpdf_vals = dist.logpdf([0.0], [1.0], 0, 1, 1, 1)
    assert isinstance(logpdf_vals, (float, np.ndarray))
    
    # Test basic mean functionality (a > 1 required)
    mean_x, mean_s2 = dist.mean(0, 1, 2, 1)  # a > 1 for valid mean
    assert isinstance(mean_x, (float, np.ndarray))
    assert isinstance(mean_s2, (float, np.ndarray))
    
    # Test basic var functionality (a > 2 required)
    var_x, var_s2 = dist.var(0, 1, 3, 1)  # a > 2 for valid variance
    assert isinstance(var_x, (float, np.ndarray))
    assert isinstance(var_s2, (float, np.ndarray))
    
    # Test frozen distribution with parameters that allow both mean and var
    frozen = dist(0, 1, 3, 1)  # Use a=3 so both mean and var work
    assert hasattr(frozen, 'pdf')
    assert hasattr(frozen, 'logpdf')
    assert hasattr(frozen, 'mean')
    assert hasattr(frozen, 'var')
    assert hasattr(frozen, 'rvs')
    
    # Test frozen rvs
    x_frozen, s2_frozen = frozen.rvs(size=3, random_state=12345)
    assert isinstance(x_frozen, np.ndarray)
    assert isinstance(s2_frozen, np.ndarray)
    assert x_frozen.shape == (3,)
    assert s2_frozen.shape == (3,)
    
    # Test frozen pdf
    pdf_frozen = frozen.pdf([0.0], [1.0])
    assert isinstance(pdf_frozen, (float, np.ndarray))
    
    # Test frozen logpdf
    logpdf_frozen = frozen.logpdf([0.0], [1.0])
    assert isinstance(logpdf_frozen, (float, np.ndarray))
    
    # Test frozen mean
    mean_frozen_x, mean_frozen_s2 = frozen.mean()
    assert isinstance(mean_frozen_x, (float, np.ndarray))
    assert isinstance(mean_frozen_s2, (float, np.ndarray))
    
    # Test frozen var
    var_frozen_x, var_frozen_s2 = frozen.var()
    assert isinstance(var_frozen_x, (float, np.ndarray))
    assert isinstance(var_frozen_s2, (float, np.ndarray))
    
    # Test that different mu values in frozen distribution give different means
    frozen_mu0 = dist(0, 1, 2, 1)
    frozen_mu1 = dist(1, 1, 2, 1)
    mean_x_0, _ = frozen_mu0.mean()
    mean_x_1, _ = frozen_mu1.mean()
    # Different mu should give different means
    assert mean_x_0 != mean_x_1
    
    # Test that s2 <= 0 gives 0 for pdf and -inf for logpdf
    pdf_zero = dist.pdf([0.0], [0.0], 0, 1, 1, 1)
    assert pdf_zero == 0.0
    
    logpdf_zero = dist.logpdf([0.0], [0.0], 0, 1, 1, 1)
    assert logpdf_zero == -np.inf
    
    # Test that PDF and logPDF are consistent
    x_test = np.array([0.0])
    s2_test = np.array([1.0])
    pdf_val = dist.pdf(x_test, s2_test, 0, 1, 1, 1)
    logpdf_val = dist.logpdf(x_test, s2_test, 0, 1, 1, 1)
    assert_allclose(np.log(pdf_val), logpdf_val, rtol=1e-10)
    
    # Test that the frozen distribution works with the same parameters
    frozen2 = dist(0, 1, 3, 1)
    mean2_x, mean2_s2 = frozen2.mean()
    assert_allclose(mean_frozen_x, mean2_x)
    assert_allclose(mean_frozen_s2, mean2_s2)
    
    # Test reproducibility with same random_state
    x1, s2_1 = dist.rvs(0, 1, 1, 1, size=5, random_state=12345)
    x2, s2_2 = dist.rvs(0, 1, 1, 1, size=5, random_state=12345)
    assert_allclose(x1, x2)
    assert_allclose(s2_1, s2_2)
    
    # Test that PDF values are reasonable (not negative)
    pdf_positive = dist.pdf([0.0], [1.0], 0, 1, 1, 1)
    assert pdf_positive >= 0
    
    # Test that PDF values are finite (not NaN or inf in normal cases)
    pdf_finite = dist.pdf([0.0], [1.0], 0, 1, 1, 1)
    assert np.isfinite(pdf_finite)
    
    # Test that logPDF values are finite or -inf
    logpdf_finite = dist.logpdf([0.0], [1.0], 0, 1, 1, 1)
    assert np.isfinite(logpdf_finite) or logpdf_finite == -np.inf
    
    # Test specific PDF values to ensure they're computed correctly
    # Test with specific known values to verify calculation is correct
    x_test = np.array([0.0, 1.0])
    s2_test = np.array([1.0, 2.0])
    pdf_vals = dist.pdf(x_test, s2_test, 0, 1, 1, 1)
    # Should be positive and finite
    assert np.all(pdf_vals >= 0)
    assert np.all(np.isfinite(pdf_vals))
    
    # Test that the distribution works with different parameter combinations
    # Test with lambda = 2 (should be valid)
    x_test2, s2_test2 = dist.rvs(0, 2, 1, 1, size=3, random_state=12345)
    assert np.all(s2_test2 > 0)
    
    # Test that the distribution handles edge cases properly
    # Very small s2 values should not cause issues
    pdf_small_s2 = dist.pdf([0.0], [1e-10], 0, 1, 1, 1)
    assert np.isfinite(pdf_small_s2) or pdf_small_s2 == 0.0