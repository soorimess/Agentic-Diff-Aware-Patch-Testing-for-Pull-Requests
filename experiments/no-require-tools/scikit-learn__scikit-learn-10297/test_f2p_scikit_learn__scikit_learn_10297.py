"""
Test for RidgeClassifierCV store_cv_values parameter
This regression test ensures that RidgeClassifierCV accepts the 
store_cv_values parameter as documented.
"""

import numpy as np
from sklearn import linear_model as lm
import pytest


def test_ridge_classifier_cv_store_cv_values_parameter_accepted():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without error."""
    # Existing tests confirm the parameter is not accepted - must be fixed
    
    # Test that the parameter is accepted, simple check that we can construct the class
    # without error (this is the main point of the bug report)
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # The parameter should be stored as an attribute
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_parameter_default():
    """Test that RidgeClassifierCV default behavior for store_cv_values."""
    # Test that default behavior works (store_cv_values should be False by default)
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True
    )
    
    # Default should be False
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is False


def test_ridge_classifier_cv_store_cv_values_parameter_false():
    """Test that RidgeClassifierCV accepts store_cv_values=False parameter."""
    # Test explicit False setting (this has same issue as True)
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=False
    )
    
    # The parameter should be stored as an attribute
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is False


def test_ridge_classifier_cv_parameter_inheritance():
    """Test that the parameter works alongside other parameters correctly."""
    # Test that all documented parameters including store_cv_values work together
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0],
        fit_intercept=True,
        normalize=False,
        scoring=None,
        cv=None,
        class_weight=None,
        store_cv_values=True
    )
    
    # All parameters should be set correctly
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True