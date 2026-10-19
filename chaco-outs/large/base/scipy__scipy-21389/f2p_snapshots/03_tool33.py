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


def test_normal_inverse_gamma_basic_functionality():
    """Test basic functionality of normal_inverse_gamma."""
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
    
    # Test basic pdf functionality (doesn't check exact values, just that it runs)
    pdf_vals = dist.pdf([0.0], [1.0], 0, 1, 1, 1)
    assert isinstance(pdf_vals, (float, np.ndarray))
    
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
    
    # Test specific behavior: mu parameter affects the mean
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