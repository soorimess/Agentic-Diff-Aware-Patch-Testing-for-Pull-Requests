"""Test regression for RidgeClassifierCV store_cv_values parameter."""
import numpy as np
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter_accepted():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without TypeError.
    
    This test ensures the fix for the bug where RidgeClassifierCV did not
    accept the store_cv_values parameter, causing:
    TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    """
    # Using binary classification labels (as expected for RidgeClassifierCV)
    n = 10
    x = np.random.randn(n, 5)
    y = np.array([0, 1] * (n // 2))  # Binary labels
    
    # This should not raise TypeError anymore
    # Before the fix, this would raise: TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 10, 0.1), 
        store_cv_values=True
    )
    
    # Parameter should be accepted and stored
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True
    
    # Also test with store_cv_values=False
    rr2 = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 10, 0.1), 
        store_cv_values=False
    )
    
    assert hasattr(rr2, 'store_cv_values')
    assert rr2.store_cv_values is False


def test_ridge_classifier_cv_store_cv_values_default_behavior():
    """Test default behavior of store_cv_values in RidgeClassifierCV.
    
    Default should be False, following the pattern of the base class.
    """
    n = 10
    x = np.random.randn(n, 5)
    y = np.array([0, 1] * (n // 2))  # Binary labels
    
    # Using default parameters - should work fine
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 10, 0.1)
    )
    
    # Should have the parameter with default value
    assert hasattr(rr, 'store_cv_values')
    # Default should be the same as _BaseRidgeCV's default
    assert rr.store_cv_values is False