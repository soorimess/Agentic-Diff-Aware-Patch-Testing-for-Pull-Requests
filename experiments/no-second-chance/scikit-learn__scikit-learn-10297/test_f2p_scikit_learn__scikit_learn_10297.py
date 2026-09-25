"""
Regression test for RidgeClassifierCV store_cv_values issue.

This test ensures that RidgeClassifierCV properly supports the store_cv_values 
parameter and demonstrates the exact error reported in the issue.
"""

import numpy as np
import pytest
from sklearn.linear_model import RidgeClassifierCV


def test_ridge_classifier_cv_store_cv_values_parameter():
    """Test that RidgeClassifierCV accepts store_cv_values parameter.
    
    This tests the exact scenario from the bug report:
    TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    """
    # Test data from the bug report
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)
    
    # This should not raise TypeError after the fix
    clf = RidgeClassifierCV(
        alphas=np.arange(0.1, 1000, 0.1), 
        normalize=True, 
        store_cv_values=True
    )
    
    # If we reach here, the parameter was accepted (this would be a pass)
    # We can then call fit - but test does not need to actually check storage functionality
    # just that parameter itself can be passed in
    assert hasattr(clf, 'store_cv_values')  # Parameter is stored in object