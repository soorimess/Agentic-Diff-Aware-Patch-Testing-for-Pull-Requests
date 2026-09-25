"""
Regression test for RidgeClassifierCV store_cv_values parameter

This test ensures RidgeClassifierCV properly accepts the store_cv_values parameter
that was missing and caused TypeError in the original bug report.
"""

import numpy as np
from sklearn.linear_model import RidgeClassifierCV


def test_ridge_classifier_cv_accepts_store_cv_values_parameter():
    """
    Test that RidgeClassifierCV accepts store_cv_values parameter.
    
    This addresses the bug where:
    TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    """
    # Exact code from bug report that was failing
    X = np.random.randn(100, 30)
    y = np.random.normal(size=100)
    
    # Before fix: This would raise TypeError
    # After fix: This should work fine
    clf = RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # If we get here without TypeError, the parameter is accepted
    assert hasattr(clf, 'store_cv_values')
    assert clf.store_cv_values is True
    
    # Should be able to fit without error
    clf.fit(X, y)
    
    # Should have cv_values_ when cv=None and store_cv_values=True
    if clf.cv is None:
        assert hasattr(clf, 'cv_values_')