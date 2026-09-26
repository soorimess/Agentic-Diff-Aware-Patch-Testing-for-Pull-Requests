"""
Test for RidgeClassifierCV store_cv_values parameter.

This test ensures that RidgeClassifierCV accepts the store_cv_values parameter
and properly stores cross-validation values when it is set to True.
"""

import numpy as np
from sklearn import linear_model as lm
from sklearn.utils.testing import assert_raises


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should not raise a TypeError
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # Should be able to fit without error
    rr.fit(x, y)
    
    # When store_cv_values=True and cv=None, cv_values_ should be set
    assert hasattr(rr, 'cv_values_'), "cv_values_ attribute should exist when store_cv_values=True"
    
    # Check the shape of cv_values_ - should be (n_samples, n_alphas)
    expected_shape = (n, len(rr.alphas))
    assert rr.cv_values_.shape == expected_shape, f"cv_values_ should have shape {expected_shape}"


def test_ridge_classifier_cv_store_cv_values_false():
    """Test that RidgeClassifierCV works with store_cv_values=False (default)."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should work without issues
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=False
    )
    
    # Should be able to fit without error
    rr.fit(x, y)
    
    # When store_cv_values=False, cv_values_ should not exist
    assert not hasattr(rr, 'cv_values_'), "cv_values_ attribute should not exist when store_cv_values=False"


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that RidgeClassifierCV works with default store_cv_values (should be False)."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should work without issues (default is False)
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True
    )
    
    # Should be able to fit without error
    rr.fit(x, y)
    
    # When store_cv_values is default (False), cv_values_ should not exist
    assert not hasattr(rr, 'cv_values_'), "cv_values_ attribute should not exist with default settings"