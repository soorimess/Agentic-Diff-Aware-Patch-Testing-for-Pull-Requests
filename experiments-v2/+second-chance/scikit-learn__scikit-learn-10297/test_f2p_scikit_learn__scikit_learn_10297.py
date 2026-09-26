"""
Test for RidgeClassifierCV store_cv_values parameter issue.

This test verifies that RidgeClassifierCV accepts and properly handles
the store_cv_values parameter, which was missing in the original implementation.
"""

import numpy as np
import pytest
from sklearn.linear_model import RidgeClassifierCV


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Create test data for binary classification
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should not raise a TypeError about unexpected keyword argument
    # The bug was that store_cv_values parameter was not accepted
    ridge_cv = RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # This should work without raising TypeError
    ridge_cv.fit(x, y)
    
    # Verify that cv_values_ attribute is set when store_cv_values=True
    assert hasattr(ridge_cv, 'cv_values_')
    assert ridge_cv.cv_values_ is not None


def test_ridge_classifier_cv_store_cv_values_false():
    """Test that RidgeClassifierCV works with store_cv_values=False (default)."""
    # Create test data for binary classification
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should work without issues
    ridge_cv = RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=False
    )
    
    ridge_cv.fit(x, y)
    
    # cv_values_ should not be set when store_cv_values=False
    assert not hasattr(ridge_cv, 'cv_values_')


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that RidgeClassifierCV works with default store_cv_values (should be False)."""
    # Create test data for binary classification
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, size=n)  # Binary classification labels
    
    # This should work without issues (default is store_cv_values=False)
    ridge_cv = RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True
    )
    
    ridge_cv.fit(x, y)
    
    # cv_values_ should not be set by default
    assert not hasattr(ridge_cv, 'cv_values_')