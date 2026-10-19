"""
Test for Mixture distribution functionality.

This test verifies that the Mixture class works as expected after the pull request
that adds mixture distributions to scipy.stats.
"""
import numpy as np
import pytest
from scipy import stats


def test_mixture_import():
    """Test that Mixture can be imported from scipy.stats"""
    # This should work after the PR is applied
    assert hasattr(stats, 'Mixture')


def test_mixture_instantiation():
    """Test that Mixture can be instantiated with components and weights"""
    # Import Normal distribution for testing
    from scipy.stats import Normal
    
    # Create components
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    
    # This should work after the PR is applied
    mixture = stats.Mixture(components, weights=weights)
    
    # Check that components and weights are stored correctly
    assert len(mixture.components) == 2
    assert np.allclose(mixture.weights, weights)


def test_mixture_pdf():
    """Test that Mixture can compute PDF values"""
    from scipy.stats import Normal
    
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    mixture = stats.Mixture(components, weights=weights)
    
    # Test PDF computation at a few points
    x = np.array([-2, 0, 1, 3])
    pdf_vals = mixture.pdf(x)
    
    # Should return array of same shape as input
    assert pdf_vals.shape == x.shape
    
    # PDF values should be non-negative
    assert np.all(pdf_vals >= 0)


def test_mixture_cdf():
    """Test that Mixture can compute CDF values"""
    from scipy.stats import Normal
    
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    mixture = stats.Mixture(components, weights=weights)
    
    # Test CDF computation at a few points
    x = np.array([-2, 0, 1, 3])
    cdf_vals = mixture.cdf(x)
    
    # Should return array of same shape as input
    assert cdf_vals.shape == x.shape
    
    # CDF values should be between 0 and 1
    assert np.all(cdf_vals >= 0)
    assert np.all(cdf_vals <= 1)


def test_mixture_mean():
    """Test that Mixture can compute mean"""
    from scipy.stats import Normal
    
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    mixture = stats.Mixture(components, weights=weights)
    
    # Compute mean
    mean_val = mixture.mean()
    
    # Should return a scalar
    assert np.isscalar(mean_val) or mean_val.shape == ()


def test_mixture_variance():
    """Test that Mixture can compute variance"""
    from scipy.stats import Normal
    
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    mixture = stats.Mixture(components, weights=weights)
    
    # Compute variance
    var_val = mixture.variance()
    
    # Should return a scalar
    assert np.isscalar(var_val) or var_val.shape == ()
    
    # Variance should be non-negative
    assert var_val >= 0


def test_mixture_sample():
    """Test that Mixture can generate samples"""
    from scipy.stats import Normal
    
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    mixture = stats.Mixture(components, weights=weights)
    
    # Generate samples
    samples = mixture.sample(1000)
    
    # Should return array of correct shape
    assert samples.shape == (1000,)
    
    # Should be able to generate samples with different shapes
    samples_2d = mixture.sample((10, 10))
    assert samples_2d.shape == (10, 10)


def test_mixture_basic_validation():
    """Test that Mixture validates basic inputs correctly"""
    from scipy.stats import Normal
    
    # Test empty components
    with pytest.raises(ValueError, match="components.*at least one"):
        stats.Mixture([])
    
    # Test invalid component type
    with pytest.raises(ValueError, match="components.*ContinuousDistribution"):
        stats.Mixture([Normal(mu=0, sigma=1), "not_a_distribution"])
    
    # Test mismatched lengths
    with pytest.raises(ValueError, match="components.*weights.*same length"):
        stats.Mixture([Normal(mu=0, sigma=1), Normal(mu=1, sigma=1)], weights=[0.5])