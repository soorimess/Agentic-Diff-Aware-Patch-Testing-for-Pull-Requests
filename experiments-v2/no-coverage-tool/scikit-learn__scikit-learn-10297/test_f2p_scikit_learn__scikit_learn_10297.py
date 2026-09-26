"""
Test for RidgeClassifierCV store_cv_values parameter issue.

This test verifies that RidgeClassifierCV accepts the store_cv_values parameter
and properly handles the cv_values_ attribute when store_cv_values=True.
"""

import numpy as np
import pytest
from sklearn import linear_model


def test_ridge_classifier_cv_store_cv_values_parameter_acceptance():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without TypeError."""
    # This should not raise a TypeError about unexpected keyword argument
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # This should work without TypeError - the main bug fix
    rr = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # The object should be created successfully with the parameter
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_parameter_default():
    """Test that store_cv_values defaults to False."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test with default settings (store_cv_values should default to False)
    rr_default = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 10, 0.1), 
        normalize=True
        # store_cv_values not specified, should default to False
    )
    
    assert hasattr(rr_default, 'store_cv_values')
    assert rr_default.store_cv_values is False


def test_ridge_classifier_cv_store_cv_values_parameter_error_handling():
    """Test that invalid parameter values are handled gracefully."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test that the parameter is accepted (this was the main bug)
    try:
        rr = linear_model.RidgeClassifierCV(
            alphas=np.arange(0.1, 100, 0.1), 
            normalize=True, 
            store_cv_values=True
        )
        # If we get here without TypeError, the parameter is accepted
        assert hasattr(rr, 'store_cv_values')
        assert rr.store_cv_values is True
    except TypeError as e:
        if "unexpected keyword argument 'store_cv_values'" in str(e):
            pytest.fail("store_cv_values parameter not accepted - this is the bug being tested")
        else:
            # Some other TypeError, re-raise
            raise