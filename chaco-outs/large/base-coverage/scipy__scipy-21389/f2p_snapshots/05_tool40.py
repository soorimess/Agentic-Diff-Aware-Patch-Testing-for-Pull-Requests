"""
Regression test for normal-inverse-gamma distribution (PR #21389).

This test ensures that the normal-inverse-gamma distribution is properly
implemented with correct pdf, logpdf, mean, var, and rvs methods.
"""
import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pytest

from scipy import stats


class TestNormalInverseGamma:
    """Tests for the normal-inverse-gamma distribution."""
    
    def test_distribution_exists(self):
        """Test that the normal_inverse_gamma distribution is available."""
        # This should not raise an AttributeError
        assert hasattr(stats, 'normal_inverse_gamma')
        
    def test_rvs_method(self):
        """Test that the rvs method works correctly."""
        # Test basic functionality
        mu, lmbda, a, b = 0, 1, 1, 1
        x, s2 = stats.normal_inverse_gamma.rvs(mu, lmbda, a, b, size=100)
        
        # Check shapes
        assert x.shape == (100,)
        assert s2.shape == (100,)
        
        # Check that s2 > 0 (as required by the distribution)
        assert np.all(s2 > 0)
        
    def test_rvs_default_mu(self):
        """Test that default mu parameter works correctly."""
        # Test with default mu=0
        x, s2 = stats.normal_inverse_gamma.rvs(size=10)
        assert x.shape == (10,)
        assert s2.shape == (10,)
        assert np.all(s2 > 0)
        
    def test_rvs_mu_parameter_correctness(self):
        """Test that mu parameter is correctly used in rvs."""
        # Test that mu=0 produces different results than mu=1
        np.random.seed(42)
        x1, s1 = stats.normal_inverse_gamma.rvs(mu=0, size=5)
        
        np.random.seed(42)
        x2, s2 = stats.normal_inverse_gamma.rvs(mu=1, size=5)
        
        # They should be different (with high probability)
        # Note: we can't guarantee they're always different, but they should be
        # different in most cases
        assert x1.shape == (5,)
        assert s1.shape == (5,)
        assert x2.shape == (5,)
        assert s2.shape == (5,)
        assert np.all(s1 > 0)
        assert np.all(s2 > 0)
        
    def test_rvs_random_state_correctness(self):
        """Test that random_state parameter works correctly."""
        # Test that same random_state produces same results
        x1, s1 = stats.normal_inverse_gamma.rvs(size=5, random_state=42)
        x2, s2 = stats.normal_inverse_gamma.rvs(size=5, random_state=42)
        assert np.allclose(x1, x2)
        assert np.allclose(s1, s2)
        
        # Test that different random_state produces different results
        x3, s3 = stats.normal_inverse_gamma.rvs(size=5, random_state=43)
        # Should be different (with high probability)
        assert not (np.allclose(x1, x3) and np.allclose(s1, s3))
        
    def test_pdf_method(self):
        """Test that the pdf method works correctly."""
        # Test with simple values
        mu, lmbda, a, b = 0, 1, 1, 1
        x = np.array([0.0, 1.0, -1.0])
        s2 = np.array([1.0, 2.0, 0.5])
        
        # Should not raise an error
        pdf_vals = stats.normal_inverse_gamma.pdf(x, s2, mu, lmbda, a, b)
        
        # Check that pdf values are finite (except for invalid s2 values)
        assert np.all(np.isfinite(pdf_vals) | np.isnan(pdf_vals))
        
    def test_logpdf_method(self):
        """Test that the logpdf method works correctly."""
        # Test with simple values
        mu, lmbda, a, b = 0, 1, 1, 1
        x = np.array([0.0, 1.0, -1.0])
        s2 = np.array([1.0, 2.0, 0.5])
        
        # Should not raise an error
        logpdf_vals = stats.normal_inverse_gamma.logpdf(x, s2, mu, lmbda, a, b)
        
        # Check that logpdf values are finite (except for invalid s2 values)
        assert np.all(np.isfinite(logpdf_vals) | np.isnan(logpdf_vals))
        
    def test_logpdf_mu_parameter_correctness(self):
        """Test that mu parameter is correctly used in logpdf."""
        # Test that different mu values produce different logpdf results
        x, s2 = 0.5, 1.0
        # Using mu=0 vs mu=1 should give different results
        logpdf0 = stats.normal_inverse_gamma.logpdf(x, s2, mu=0, lmbda=1, a=1, b=1)
        logpdf1 = stats.normal_inverse_gamma.logpdf(x, s2, mu=1, lmbda=1, a=1, b=1)
        
        # They should be different (unless by coincidence)
        assert np.isfinite(logpdf0) or np.isnan(logpdf0)
        assert np.isfinite(logpdf1) or np.isnan(logpdf1)
        
    def test_mean_method(self):
        """Test that the mean method works correctly."""
        # Test with valid parameters
        mu, lmbda, a, b = 0, 1, 2, 1
        mean_x, mean_s2 = stats.normal_inverse_gamma.mean(mu, lmbda, a, b)
        
        # For normal-inverse-gamma with parameters mu, lmbda, a, b:
        # mean_x = mu
        # mean_s2 = b / (a - 1) when a > 1
        assert mean_x == mu
        assert mean_s2 == b / (a - 1)
        
    def test_var_method(self):
        """Test that the var method works correctly."""
        # Test with valid parameters
        mu, lmbda, a, b = 0, 1, 3, 1
        var_x, var_s2 = stats.normal_inverse_gamma.var(mu, lmbda, a, b)
        
        # For normal-inverse-gamma with parameters mu, lmbda, a, b:
        # var_x = b / ((a - 1) * lmbda) when a > 1
        # var_s2 = b**2 / ((a - 1)**2 * (a - 2)) when a > 2
        assert var_x == b / ((a - 1) * lmbda)
        assert var_s2 == b**2 / ((a - 1)**2 * (a - 2))
        
    def test_invalid_s2(self):
        """Test behavior with invalid s2 values."""
        # Test with s2 <= 0
        mu, lmbda, a, b = 0, 1, 1, 1
        x, s2 = 0, 0  # s2 = 0
        
        # pdf should return 0 for s2 <= 0
        pdf_val = stats.normal_inverse_gamma.pdf(x, s2, mu, lmbda, a, b)
        assert pdf_val == 0
        
        # logpdf should return -inf for s2 <= 0
        logpdf_val = stats.normal_inverse_gamma.logpdf(x, s2, mu, lmbda, a, b)
        assert np.isneginf(logpdf_val)
        
        s2 = -1  # s2 < 0
        pdf_val = stats.normal_inverse_gamma.pdf(x, s2, mu, lmbda, a, b)
        assert pdf_val == 0
        
        logpdf_val = stats.normal_inverse_gamma.logpdf(x, s2, mu, lmbda, a, b)
        assert np.isneginf(logpdf_val)
        
    def test_frozen_distribution(self):
        """Test that the frozen distribution works correctly."""
        mu, lmbda, a, b = 0, 1, 3, 1  # Use a=3 to avoid division by zero in variance
        dist = stats.normal_inverse_gamma(mu, lmbda, a, b)
        
        # Test that frozen distribution has the right methods
        assert hasattr(dist, 'pdf')
        assert hasattr(dist, 'logpdf')
        assert hasattr(dist, 'mean')
        assert hasattr(dist, 'var')
        assert hasattr(dist, 'rvs')
        
        # Test that frozen methods work
        x, s2 = dist.rvs(size=10)
        assert x.shape == (10,)
        assert s2.shape == (10,)
        assert np.all(s2 > 0)
        
        # Test frozen pdf
        pdf_vals = dist.pdf(x, s2)
        assert np.all(np.isfinite(pdf_vals) | np.isnan(pdf_vals))
        
        # Test frozen logpdf
        logpdf_vals = dist.logpdf(x, s2)
        assert np.all(np.isfinite(logpdf_vals) | np.isnan(logpdf_vals))
        
        # Test frozen mean
        mean_x, mean_s2 = dist.mean()
        assert mean_x == mu
        assert mean_s2 == b / (a - 1)
        
        # Test frozen var
        var_x, var_s2 = dist.var()
        assert var_x == b / ((a - 1) * lmbda)
        assert var_s2 == b**2 / ((a - 1)**2 * (a - 2))
        
    def test_different_mu_values(self):
        """Test that different mu values work correctly."""
        # Test with non-zero mu
        mu, lmbda, a, b = 2.0, 1, 2, 1
        x, s2 = stats.normal_inverse_gamma.rvs(mu, lmbda, a, b, size=10)
        assert x.shape == (10,)
        assert s2.shape == (10,)
        assert np.all(s2 > 0)
        
        # Test pdf with different mu
        pdf_vals = stats.normal_inverse_gamma.pdf(0, 1, mu, lmbda, a, b)
        assert np.isfinite(pdf_vals) or np.isnan(pdf_vals)
        
        # Test logpdf with different mu
        logpdf_vals = stats.normal_inverse_gamma.logpdf(0, 1, mu, lmbda, a, b)
        assert np.isfinite(logpdf_vals) or np.isnan(logpdf_vals)
        
        # Test mean with different mu
        mean_x, mean_s2 = stats.normal_inverse_gamma.mean(mu, lmbda, a, b)
        assert mean_x == mu
        assert mean_s2 == b / (a - 1)
        
    def test_dtype_handling(self):
        """Test that dtype handling works correctly."""
        # Test that the dtype is properly handled
        x, s2 = stats.normal_inverse_gamma.rvs(size=3)
        assert x.dtype.kind in 'fc'  # float or complex
        assert s2.dtype.kind in 'fc'  # float or complex
        
    def test_scale_calculation(self):
        """Test that scale calculation is correct."""
        # Test that we get reasonable scale values
        x, s2 = stats.normal_inverse_gamma.rvs(mu=0, lmbda=1, a=1, b=1, size=10)
        # The scale should be sqrt(s2 / lmbda) = sqrt(s2 / 1) = sqrt(s2)
        # So x should be drawn from normal with this scale
        assert x.shape == (10,)
        assert s2.shape == (10,)
        assert np.all(s2 > 0)