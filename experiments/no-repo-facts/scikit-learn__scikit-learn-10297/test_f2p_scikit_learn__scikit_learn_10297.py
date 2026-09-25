"""
Test for RidgeClassifierCV store_cv_values parameter support
This test verifies that the fix in RidgeClassifierCV allows store_cv_values parameter to be accepted
"""

import numpy as np
from sklearn.linear_model import RidgeClassifierCV
from sklearn.utils.testing import assert_equal
from sklearn.utils.testing import assert_true


def test_ridge_classifier_cv_accepts_store_cv_values_parameter():
    """
    Test that RidgeClassifierCV accepts the store_cv_values parameter.
    
    Before the fix, this would raise:
    TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    
    After the fix, this should work without error.
    """
    # Test the exact case from the bug report
    alphas = np.arange(0.1, 1000, 0.1)
    
    # This should NOT raise a TypeError
    clf = RidgeClassifierCV(alphas=alphas, normalize=True, store_cv_values=True)
    
    # Verify the parameter was accepted and stored
    assert_true(hasattr(clf, 'store_cv_values'))
    assert_equal(clf.store_cv_values, True)
    
    # Test default behavior
    clf_default = RidgeClassifierCV(alphas=alphas)
    assert_equal(clf_default.store_cv_values, False)


def test_ridge_classifier_cv_parameter_compatibility():
    """
    Test that the store_cv_values parameter doesn't interfere with other parameters.
    """
    alphas = np.arange(0.1, 10, 0.1)
    
    # Test various combinations
    clf1 = RidgeClassifierCV(alphas=alphas, store_cv_values=True)
    assert_equal(clf1.store_cv_values, True)
    
    clf2 = RidgeClassifierCV(alphas=alphas, store_cv_values=False)
    assert_equal(clf2.store_cv_values, False)
    
    clf3 = RidgeClassifierCV(alphas=alphas, store_cv_values=True, class_weight='balanced')
    assert_equal(clf3.store_cv_values, True)


if __name__ == "__main__":
    test_ridge_classifier_cv_accepts_store_cv_values_parameter()
    test_ridge_classifier_cv_parameter_compatibility()
    print("All tests passed!")