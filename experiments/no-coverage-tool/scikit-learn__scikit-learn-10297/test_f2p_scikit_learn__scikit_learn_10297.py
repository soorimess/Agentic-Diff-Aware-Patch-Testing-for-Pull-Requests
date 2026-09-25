"""Test for RidgeClassifierCV store_cv_values parameter regression."""

import numpy as np
from sklearn import linear_model


def test_ridge_classifier_cv_store_cv_values_parameter_accepted():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without TypeError.
    
    This test ensures that the bug reported in the issue is fixed:
    "TypeError: __init__() got an unexpected keyword argument 'store_cv_values'"
    """
    # This tests the exact bug scenario - before fix this would raise TypeError
    X = np.random.randn(10, 5) 
    y = np.random.randint(0, 2, 10)
    
    # Before the fix, this would raise:
    # TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    # After the fix, it should work correctly
    ridge = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 10.0, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # Verify the parameter is correctly accepted and stored
    assert hasattr(ridge, 'store_cv_values')
    assert ridge.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_defaults_to_false():
    """Test that store_cv_values parameter defaults to False."""
    X = np.random.randn(10, 5)
    y = np.random.randint(0, 2, 10)
    
    # Default behavior should still work
    ridge = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 10.0, 0.1), 
        normalize=True
    )
    
    assert hasattr(ridge, 'store_cv_values')
    assert ridge.store_cv_values is False


if __name__ == "__main__":
    # Run tests manually if needed
    test_ridge_classifier_cv_store_cv_values_parameter_accepted()
    test_ridge_classifier_cv_store_cv_values_defaults_to_false()
    print("All regression tests passed!")