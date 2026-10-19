"""
Test for Mixture distribution functionality.

This test file verifies the behavior of the new Mixture class that was added
in pull request #21700. The test ensures that the Mixture class is properly
available and functional.
"""

import numpy as np
import pytest


def test_mixture_exists_and_works():
    """
    Test that Mixture class exists and works correctly.
    
    This test will fail with ImportError if Mixture is not available (old code)
    and should pass if Mixture is available (new code).
    """
    # Try to import Mixture - this should work after the PR
    from scipy.stats import Mixture
    
    # Import Normal distribution for testing
    from scipy.stats import Normal
    
    # Create components
    components = [Normal(mu=-1.2, sigma=1.1), Normal(mu=1.3, sigma=0.9)]
    weights = [0.4, 0.6]
    
    # Create mixture - this should work after the PR
    mixture = Mixture(components, weights=weights)
    
    # Test that it has expected methods
    assert hasattr(mixture, 'pdf')
    assert hasattr(mixture, 'logpdf')
    assert hasattr(mixture, 'cdf')
    assert hasattr(mixture, 'icdf')
    
    # Test PDF evaluation
    x = np.array([-2, 0, 2])
    pdf_values = mixture.pdf(x)
    assert pdf_values is not None
    assert isinstance(pdf_values, np.ndarray)
    assert len(pdf_values) == len(x)
    
    # PDF values should be non-negative
    assert np.all(pdf_values >= 0)
    
    # Test logPDF evaluation
    logpdf_values = mixture.logpdf(x)
    assert logpdf_values is not None
    assert isinstance(logpdf_values, np.ndarray)
    assert len(logpdf_values) == len(x)
    
    # Test that components and weights are accessible
    assert hasattr(mixture, 'components')
    assert hasattr(mixture, 'weights')
    
    # Test that components are properly stored
    assert len(mixture.components) == len(components)
    assert len(mixture.weights) == len(weights)
    
    # Test that weights sum to 1.0
    assert np.isclose(np.sum(mixture.weights), 1.0)


def test_mixture_validation_empty_components():
    """
    Test that Mixture properly validates empty components.
    
    This ensures that the validation logic for empty components works correctly.
    """
    from scipy.stats import Mixture
    
    # Test empty components - should raise ValueError with specific message
    with pytest.raises(ValueError, match="at least one random variable"):
        Mixture([])