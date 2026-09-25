"""
Regression test for RidgeClassifierCV's store_cv_values parameter issue.

This test ensures that RidgeClassifierCV properly supports the store_cv_values
parameter, which was missing from its __init__ method in the original code.
"""

import numpy as np
import pytest
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # This should not raise a TypeError
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # This should work without raising TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # Check that we can access the parameter after initialization
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values == True


def test_ridge_classifier_cv_store_cv_values_parameter_false():
    """Test that RidgeClassifierCV accepts store_cv_values=False parameter."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # This should work without raising TypeError even with store_cv_values=False
    rr = lm.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1), 
        normalize=True, 
        store_cv_values=False
    )
    
    # Check that we can access the parameter after initialization
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values == False


def test_ridge_classifier_cv_store_cv_values_default():
    """Test that default behavior still works (store_cv_values=False by default)."""
    n = 20
    x = np.random.randn(n, 5)
    y = (x[:, 0] + x[:, 1] > 0).astype(int)
    
    # Should work with default parameters (store_cv_values should be False by default)
    rr = lm.RidgeClassifierCV(
        alphas=[0.1, 1.0, 10.0]
        # No store_cv_values specified - should default to False
    )
    
    # Should not raise error
    rr.fit(x, y)
    
    # Should be able to access store_cv_values attribute 
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values == False


if __name__ == "__main__":
    # Run the tests to make sure they work correctly
    test_ridge_classifier_cv_store_cv_values_parameter()
    test_ridge_classifier_cv_store_cv_values_parameter_false()
    test_ridge_classifier_cv_store_cv_values_default()
    print("All tests passed!")