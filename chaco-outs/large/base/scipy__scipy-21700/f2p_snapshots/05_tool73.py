"""
Regression tests for Mixture distribution functionality.

This test file ensures that the Mixture distribution class works correctly
as added in pull request #21700.
"""

import numpy as np
import pytest
from scipy import stats


def test_mixture_import():
    """Test that Mixture class can be imported from scipy.stats"""
    # This test is designed to pass after the PR is applied
    # In current state, it will fail because Mixture doesn't exist yet
    from scipy.stats import Mixture
    assert Mixture is not None


def test_mixture_basic_functionality():
    """Test basic Mixture distribution functionality"""
    # This test is designed to pass after the PR is applied
    from scipy.stats import Mixture, Normal
    
    # Create simple mixture of two normal distributions
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    
    # This should work after the PR
    X = Mixture(components, weights=weights)
    
    # Test that components and weights are accessible
    assert len(X.components) == 2
    assert len(X.weights) == 2
    assert np.allclose(X.weights, weights)
    
    # Test basic methods work
    x = np.array([0.0])
    pdf_val = X.pdf(x)
    logpdf_val = X.logpdf(x)
    
    # Should return finite values
    assert np.isfinite(pdf_val)
    assert np.isfinite(logpdf_val)


def test_mixture_moments():
    """Test moment calculation in Mixture distribution"""
    from scipy.stats import Mixture, Normal
    
    # Create mixture with known moments
    components = [Normal(mu=-1.0, sigma=0.5), Normal(mu=1.0, sigma=0.5)]
    X = Mixture(components, weights=[0.3, 0.7])
    
    # Test mean calculation
    mean_val = X.mean()
    assert np.isfinite(mean_val)
    
    # Test variance calculation
    var_val = X.variance()
    assert np.isfinite(var_val)
    assert var_val >= 0
    
    # Test standard deviation
    std_val = X.standard_deviation()
    assert np.isfinite(std_val)
    assert std_val >= 0
    
    # Test skewness
    skew_val = X.skewness()
    assert np.isfinite(skew_val)
    
    # Test kurtosis
    kurt_val = X.kurtosis()
    assert np.isfinite(kurt_val)


def test_mixture_sample():
    """Test sampling from Mixture distribution"""
    from scipy.stats import Mixture, Normal
    
    # Create mixture
    components = [Normal(mu=-1.0, sigma=0.5), Normal(mu=1.0, sigma=0.5)]
    X = Mixture(components, weights=[0.3, 0.7])
    
    # Test sampling
    sample = X.sample(100)
    assert sample.shape == (100,)
    
    # Test sampling with different shape
    sample2 = X.sample((10, 5))
    assert sample2.shape == (10, 5)


def test_mixture_validation():
    """Test input validation in Mixture class"""
    from scipy.stats import Mixture, Normal
    
    # Test empty components - check exact error message
    with pytest.raises(ValueError) as exc_info:
        Mixture([])
    assert "components" in str(exc_info.value).lower()
    assert "at least one" in str(exc_info.value).lower()
    
    # Test invalid component type - check exact error message
    with pytest.raises(ValueError) as exc_info:
        Mixture([1, 2, 3])  # Not ContinuousDistribution instances
    assert "instance" in str(exc_info.value).lower()
    assert "ContinuousDistribution" in str(exc_info.value)
    
    # Test mismatched lengths - check exact error message
    with pytest.raises(ValueError) as exc_info:
        Mixture([Normal(mu=0, sigma=1)], weights=[0.5, 0.5])
    assert "components" in str(exc_info.value).lower()
    assert "weights" in str(exc_info.value).lower()
    assert "same length" in str(exc_info.value).lower()
    
    # Test invalid weights (not summing to 1) - check exact error message
    with pytest.raises(ValueError) as exc_info:
        Mixture([Normal(mu=0, sigma=1), Normal(mu=1, sigma=1)], weights=[0.3, 0.4])
    assert "weights" in str(exc_info.value).lower()
    assert "sum to 1" in str(exc_info.value).lower()
    
    # Test negative weights - check that it raises a ValueError
    try:
        Mixture([Normal(mu=0, sigma=1), Normal(mu=1, sigma=1)], weights=[0.5, -0.5])
        # If we get here without exception, that's also a problem
        assert False, "Should have raised ValueError for negative weights"
    except ValueError:
        # This is expected - the exact message may vary
        pass


def test_mixture_support_and_entropy():
    """Test support and entropy methods in Mixture distribution"""
    from scipy.stats import Mixture, Normal
    
    # Create mixture
    components = [Normal(mu=-2.0, sigma=0.5), Normal(mu=2.0, sigma=0.5)]
    X = Mixture(components, weights=[0.5, 0.5])
    
    # Test support method
    support_lower, support_upper = X.support()
    # Should be finite bounds (infinite support from normal distributions)
    # But since we're testing that the method works, we just check it doesn't crash
    assert support_lower is not None
    assert support_upper is not None
    
    # Test that we can call entropy methods without error
    # These should not raise NotImplementedError (they should be implemented)
    try:
        entropy_val = X.entropy()
        assert np.isfinite(entropy_val) or np.isnan(entropy_val)
    except NotImplementedError:
        # If it raises NotImplementedError, that's a problem with the implementation
        pytest.fail("entropy method should not raise NotImplementedError")
    
    try:
        logentropy_val = X.logentropy()
        assert np.isfinite(logentropy_val) or np.isnan(logentropy_val)
    except NotImplementedError:
        # If it raises NotImplementedError, that's a problem with the implementation
        pytest.fail("logentropy method should not raise NotImplementedError")