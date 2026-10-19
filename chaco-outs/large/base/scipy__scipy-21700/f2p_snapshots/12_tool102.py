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
    
    # Test raw moments
    try:
        moment_1 = X.moment(1, kind='raw')
        assert np.isfinite(moment_1)
        
        moment_2 = X.moment(2, kind='raw')
        assert np.isfinite(moment_2)
    except NotImplementedError:
        pytest.fail("moment method should not raise NotImplementedError")


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


def test_mixture_comprehensive_methods():
    """Test comprehensive methods in Mixture distribution"""
    from scipy.stats import Mixture, Normal
    
    # Create mixture
    components = [Normal(mu=-1.0, sigma=0.5), Normal(mu=1.0, sigma=0.5)]
    X = Mixture(components, weights=[0.3, 0.7])
    
    # Test mode method - should not raise NotImplementedError
    try:
        mode_val = X.mode()
        assert np.isfinite(mode_val)
    except NotImplementedError:
        # If it raises NotImplementedError, that's a problem with the implementation
        pytest.fail("mode method should not raise NotImplementedError")
    
    # Test inverse CDF method
    try:
        # This should work - test with a valid probability
        icdf_val = X.icdf(0.5)
        assert np.isfinite(icdf_val)
    except NotImplementedError:
        # If it raises NotImplementedError, that's a problem with the implementation
        pytest.fail("icdf method should not raise NotImplementedError")
    
    # Test inverse CCDF method
    try:
        # This should work - test with a valid probability
        iccdf_val = X.iccdf(0.5)
        assert np.isfinite(iccdf_val)
    except NotImplementedError:
        # If it raises NotImplementedError, that's a problem with the implementation
        pytest.fail("iccdf method should not raise NotImplementedError")
    
    # Test logccdf method
    try:
        # Test with single value
        logccdf_val = X.logccdf(0.0)
        assert np.isfinite(logccdf_val)
        
        # Test with array
        logccdf_vals = X.logccdf([0.0, 1.0])
        assert isinstance(logccdf_vals, np.ndarray)
        assert logccdf_vals.shape == (2,)
        assert np.all(np.isfinite(logccdf_vals))
    except NotImplementedError:
        pytest.fail("logccdf method should not raise NotImplementedError")
    
    # Test that methods work properly
    try:
        # Test with a few different probabilities
        p_vals = [0.1, 0.25, 0.5, 0.75, 0.9]
        for p in p_vals:
            icdf_val = X.icdf(p)
            assert np.isfinite(icdf_val)
    except NotImplementedError:
        pytest.fail("icdf method should not raise NotImplementedError")