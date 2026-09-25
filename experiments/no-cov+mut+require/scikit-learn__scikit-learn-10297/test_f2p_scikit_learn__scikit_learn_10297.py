"""
Regression test for RidgeClassifierCV store_cv_values issue.

This test ensures that RidgeClassifierCV supports the store_cv_values
parameter that was missing in the original implementation.
"""

import numpy as np
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Create test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # This should not raise TypeError about unexpected keyword argument
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        normalize=True, 
        store_cv_values=True
    )
    
    # Verify we can fit the model
    rr.fit(x, y)
    
    # Verify that cv_values_ attribute exists when store_cv_values=True
    assert hasattr(rr, 'cv_values_'), "cv_values_ should exist when store_cv_values=True"
    assert rr.cv_values_ is not None, "cv_values_ should not be None"


def test_ridge_classifier_cv_store_cv_values_false():
    """Test that RidgeClassifierCV works with store_cv_values=False."""
    # Create test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # This should work fine with default store_cv_values=False
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        normalize=True, 
        store_cv_values=False
    )
    
    # Verify we can fit the model
    rr.fit(x, y)
    
    # cv_values_ should not be present when store_cv_values=False
    assert not hasattr(rr, 'cv_values_') or rr.cv_values_ is None


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that RidgeClassifierCV works with default store_cv_values parameter."""
    # Create test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # This should work fine with default store_cv_values=False
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        normalize=True
        # store_cv_values not specified, should default to False
    )
    
    # Verify we can fit the model
    rr.fit(x, y)
    
    # cv_values_ should not be present when store_cv_values=False (default)
    assert not hasattr(rr, 'cv_values_') or rr.cv_values_ is None


def test_ridge_classifier_cv_store_cv_values_with_cv_none():
    """Test that RidgeClassifierCV works with store_cv_values=True when cv=None."""
    # Create test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # This should work fine when cv=None (and store_cv_values=True)
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        normalize=True, 
        store_cv_values=True,
        cv=None  # This is the default and what's required for store_cv_values to work
    )
    
    # Verify we can fit the model
    rr.fit(x, y)
    
    # Verify that cv_values_ attribute exists when store_cv_values=True
    assert hasattr(rr, 'cv_values_'), "cv_values_ should exist when store_cv_values=True"
    assert rr.cv_values_ is not None, "cv_values_ should not be None"
    
    # Check that cv_values_ has expected shape: (n_samples, n_alphas) 
    expected_shape = (n, len(np.arange(0.1, 100, 10)))
    assert rr.cv_values_.shape == expected_shape, f"cv_values_ shape {rr.cv_values_.shape} doesn't match expected {expected_shape}"