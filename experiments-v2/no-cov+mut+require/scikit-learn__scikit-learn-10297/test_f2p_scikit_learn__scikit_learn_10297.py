"""
Regression test for RidgeClassifierCV store_cv_values parameter issue.

This test ensures that RidgeClassifierCV properly accepts and handles the
store_cv_values parameter, which was missing in the original implementation.
"""
import numpy as np
import pytest


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter without error."""
    # This should not raise a TypeError
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test that store_cv_values parameter can be passed without error
    rr = pytest.importorskip('sklearn.linear_model').RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    # This should not raise TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is True


def test_ridge_classifier_cv_store_cv_values_with_cv_none():
    """Test that cv_values_ is set when store_cv_values=True and cv=None."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test with cv=None (default) and store_cv_values=True
    rr = pytest.importorskip('sklearn.linear_model').RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        cv=None,  # This is the default
        store_cv_values=True
    )
    
    # This should not raise an error and should set cv_values_
    rr.fit(x, y)
    
    # cv_values_ should be set when store_cv_values=True and cv=None
    assert hasattr(rr, 'cv_values_')
    assert rr.cv_values_ is not None
    # Should have shape (n_samples, n_alphas) for single target
    assert rr.cv_values_.shape == (n, len(rr.alphas))


def test_ridge_classifier_cv_store_cv_values_with_cv_not_none():
    """Test that error is raised when store_cv_values=True and cv is not None."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test with cv=3 and store_cv_values=True - should raise ValueError
    rr = pytest.importorskip('sklearn.linear_model').RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10), 
        cv=3,  # Not None
        store_cv_values=True
    )
    
    # This should raise ValueError because store_cv_values=True is incompatible with cv!=None
    with pytest.raises(ValueError, match="cv!=None and store_cv_values=True are incompatible"):
        rr.fit(x, y)


def test_ridge_classifier_cv_store_cv_values_default_false():
    """Test that default store_cv_values is False."""
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # Test default behavior
    rr = pytest.importorskip('sklearn.linear_model').RidgeClassifierCV(
        alphas=np.arange(0.1, 100, 10)
    )
    
    assert hasattr(rr, 'store_cv_values')
    assert rr.store_cv_values is False
    
    rr.fit(x, y)
    
    # cv_values_ should not be set when store_cv_values=False (default)
    assert not hasattr(rr, 'cv_values_')