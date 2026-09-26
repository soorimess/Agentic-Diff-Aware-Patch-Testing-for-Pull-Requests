"""
Test for RidgeClassifierCV store_cv_values parameter.

This test ensures that RidgeClassifierCV accepts and properly handles
the store_cv_values parameter, which was missing from the implementation.
"""
import numpy as np
import pytest
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # This should not raise a TypeError about unexpected keyword argument
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # The object should be created successfully
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_false():
    """Test that store_cv_values=False works correctly."""
    # Test data
    n = 50
    x = np.random.randn(n, 10)
    y = np.random.randint(0, 2, size=n)
    
    # Create classifier with store_cv_values=False (default)
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0], 
        cv=None,  # This is required for store_cv_values to work
        store_cv_values=False
    )
    
    # Fit the model
    rr.fit(x, y)
    
    # Check that cv_values_ attribute is not created when store_cv_values=False
    assert hasattr(rr, 'cv_values_') is False