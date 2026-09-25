"""
Test for RidgeClassifierCV store_cv_values parameter
This is a regression test for the bug where RidgeClassifierCV
did not support the store_cv_values parameter.
"""
import numpy as np
import pytest
from sklearn import linear_model


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter."""
    # Test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # This should not raise TypeError (the main bug reported)
    rr = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1),
        normalize=True,
        store_cv_values=True  # This was causing TypeError before fix
    )
    
    # This should work without error
    rr.fit(x, y)
    
    # The cv_values_ attribute should be present when store_cv_values=True
    assert hasattr(rr, 'cv_values_')
    assert rr.cv_values_ is not None


def test_ridge_classifier_cv_store_cv_values_default_false():
    """Test that RidgeClassifierCV defaults store_cv_values to False."""
    # Test data  
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # Default should work without error
    rr = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1),
        normalize=True
    )
    
    # This should work without error
    rr.fit(x, y)
    
    # The cv_values_ attribute should not be present by default
    assert not hasattr(rr, 'cv_values_')


def test_ridge_classifier_cv_store_cv_values_with_cv_none():
    """Test that RidgeClassifierCV works with store_cv_values=True and cv=None."""
    # Test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # When cv=None (default), store_cv_values should work
    rr = linear_model.RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 0.1),
        cv=None,
        store_cv_values=True
    )
    
    rr.fit(x, y)
    
    # cv_values_ should be available and have correct shape
    assert hasattr(rr, 'cv_values_')
    # Shape should be (n_samples, n_alphas)
    expected_shape = (n, len(np.arange(0.1, 100, 0.1)))
    assert rr.cv_values_.shape == expected_shape


def test_ridge_classifier_cv_store_cv_values_with_cv_not_none_error():
    """Test that RidgeClassifierCV raises error with store_cv_values=True and cv!=None."""
    # Test data
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.randint(0, 2, n)  # Binary classification
    
    # When cv is specified, store_cv_values should raise an error
    # This should work after the fix (the error case should continue to work)
    with pytest.raises(ValueError, match="cv!=None and store_cv_values=True"):
        rr = linear_model.RidgeClassifierCV(
            alphas=np.arange(0.1, 100, 0.1),
            cv=3,  # Specify cv, not None
            store_cv_values=True
        )
        rr.fit(x, y)