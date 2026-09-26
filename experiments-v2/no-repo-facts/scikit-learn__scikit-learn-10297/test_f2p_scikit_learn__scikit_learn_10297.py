"""Test for RidgeClassifierCV store_cv_values parameter bug.

This test ensures that RidgeClassifierCV accepts and properly handles 
the store_cv_values parameter as documented.
"""

import numpy as np
from sklearn import linear_model as lm


def test_ridge_classifier_cv_store_cv_values_functionality():
    """Test that RidgeClassifierCV store_cv_values functionality works correctly."""
    # Test with a simple case
    x = np.array([[-1, -1], [-1, 0], [-.8, -1], [1, 1], [1, 0]])
    y = np.array([1, 1, 1, -1, -1])
    
    # Test with store_cv_values=True - this should work after the fix
    try:
        rr_with_cv = lm.RidgeClassifierCV(
            alphas=[0.01, 0.1, 1], 
            store_cv_values=True
        )
        rr_with_cv.fit(x, y)
        
        # Should have cv_values_ attribute when store_cv_values=True and cv=None
        assert hasattr(rr_with_cv, 'cv_values_'), "cv_values_ should exist when store_cv_values=True"
        assert rr_with_cv.cv_values_ is not None, "cv_values_ should not be None"
        
        # Test that it works with store_cv_values=False too
        rr_without_cv = lm.RidgeClassifierCV(
            alphas=[0.01, 0.1, 1], 
            store_cv_values=False
        )
        rr_without_cv.fit(x, y)
        
        # Should not crash and should have the basic attributes
        assert hasattr(rr_without_cv, 'alpha_'), "Should have alpha_ attribute"
        
        # Test default behavior
        rr_default = lm.RidgeClassifierCV(alphas=[0.01, 0.1, 1])
        rr_default.fit(x, y)
        assert hasattr(rr_default, 'alpha_'), "Should have alpha_ attribute with default settings"
        
    except TypeError as e:
        if "store_cv_values" in str(e):
            raise AssertionError("RidgeClassifierCV should accept store_cv_values parameter") from e
        else:
            raise


if __name__ == "__main__":
    test_ridge_classifier_cv_store_cv_values_functionality()
    print("Test passed!")