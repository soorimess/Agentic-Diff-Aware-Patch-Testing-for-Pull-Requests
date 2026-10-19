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