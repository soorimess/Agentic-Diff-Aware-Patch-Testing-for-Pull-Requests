"""
Test for RidgeClassifierCV store_cv_values parameter issue.
This test verifies that RidgeClassifierCV properly supports the store_cv_values parameter.
"""
import numpy as np
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without error."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should not raise a TypeError - the main bug being tested
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # This should not raise a TypeError
    rr.fit(x, y)
    
    # When store_cv_values=True, cv_values_ should be available
    assert hasattr(rr, 'cv_values_'), "cv_values_ attribute should be present when store_cv_values=True"
    assert rr.cv_values_ is not None, "cv_values_ should not be None when store_cv_values=True"


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that RidgeClassifierCV default behavior works correctly."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # Default behavior should work without issues
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True
        # store_cv_values not specified, should default to False
    )
    
    # This should not raise a TypeError
    rr.fit(x, y)
    
    # The important thing is that it doesn't raise an error
    assert hasattr(rr, 'alpha_'), "alpha_ should be present after fitting"