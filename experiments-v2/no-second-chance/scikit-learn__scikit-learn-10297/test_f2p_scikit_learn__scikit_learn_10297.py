"""
Test for RidgeClassifierCV store_cv_values parameter.

This test ensures that RidgeClassifierCV accepts and properly handles
the store_cv_values parameter, which was missing in the implementation.
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
    
    # This should not raise a TypeError
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # The parameter should be accepted and stored
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_functionality():
    """Test that RidgeClassifierCV with store_cv_values=True actually stores cv values."""
    # Test data
    n = 50
    x = np.random.randn(n, 10)
    y = np.random.randint(0, 2, size=n)  # Binary classification
    
    # Create classifier with store_cv_values=True
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0], 
        cv=None,  # This is required for store_cv_values to work
        store_cv_values=True
    )
    
    # Fit the model
    rr.fit(x, y)
    
    # Check that cv_values_ attribute is created
    assert hasattr(rr, 'cv_values_')
    
    # cv_values_ should be an array with shape (n_samples, n_alphas) 
    # when cv=None and store_cv_values=True
    expected_shape = (n, len(rr.alphas))
    assert rr.cv_values_.shape == expected_shape


def test_ridge_classifier_cv_store_cv_values_default_false():
    """Test that store_cv_values defaults to False."""
    # Test data
    n = 50
    x = np.random.randn(n, 10)
    y = np.random.randint(0, 2, size=n)
    
    # Create classifier without specifying store_cv_values
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0], 
        cv=None
    )
    
    # Default should be False
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is False
    
    # Fit the model
    rr.fit(x, y)
    
    # cv_values_ should not be present when store_cv_values=False
    assert not hasattr(rr, 'cv_values_')


def test_ridge_classifier_cv_store_cv_values_with_cv():
    """Test that store_cv_values works with cv parameter when cv=None."""
    # Test data
    n = 50
    x = np.random.randn(n, 10)
    y = np.random.randint(0, 2, size=n)
    
    # Create classifier with store_cv_values=True and cv=None
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0], 
        cv=None,  # Required for store_cv_values to work
        store_cv_values=True
    )
    
    # Fit the model
    rr.fit(x, y)
    
    # Check that cv_values_ attribute is created
    assert hasattr(rr, 'cv_values_')
    
    # cv_values_ should be an array with shape (n_samples, n_alphas) 
    expected_shape = (n, len(rr.alphas))
    assert rr.cv_values_.shape == expected_shape