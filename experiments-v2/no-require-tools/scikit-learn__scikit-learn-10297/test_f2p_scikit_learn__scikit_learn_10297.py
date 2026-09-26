"""Test for RidgeClassifierCV store_cv_values parameter bug.

This test verifies that RidgeClassifierCV accepts and properly handles
the store_cv_values parameter, which was missing from the implementation
before the fix.
"""

import numpy as np
import pytest
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification labels
    
    # This should not raise a TypeError - reproducing the exact example from the bug report
    # The bug was that store_cv_values parameter was not accepted at all
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # This should work without error
    rr.fit(x, y)
    
    # The cv_values_ attribute should be set when store_cv_values=True
    assert hasattr(rr, 'cv_values_')
    assert rr.cv_values_ is not None


def test_ridge_classifier_cv_store_cv_values_false():
    """Test that RidgeClassifierCV works with store_cv_values=False."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification labels
    
    # This should not raise a TypeError
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=False
    )
    
    # This should work without error
    rr.fit(x, y)
    
    # The cv_values_ attribute should not be set when store_cv_values=False
    assert not hasattr(rr, 'cv_values_') or rr.cv_values_ is None


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that RidgeClassifierCV works with default store_cv_values."""
    # Test data - proper classification data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification labels
    
    # This should work with default store_cv_values=False
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True
    )
    
    # This should work without error
    rr.fit(x, y)
    
    # The cv_values_ attribute should not be set by default
    assert not hasattr(rr, 'cv_values_') or rr.cv_values_ is None