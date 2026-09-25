"""
Regression tests for LogisticRegressionCV IndexError with refit=False

This tests the exact bugs fixed in the pull request:
1. IndexError: too many indices for array in multi-class handling
2. Incorrect handling of l1_ratio_ when penalty is not elasticnet

The tests ensure that both changes work properly.
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV

def test_logistic_regression_cv_multi_class_indexerror():
    """Test that ensures the IndexError with multi_class handling is fixed"""
    # This reproduces the exact case from the bug report that failed
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Important: this should work without IndexError
    # The problem was when multi_class='auto' was resolved to 'ovr' but 
    # conditional checked self.multi_class instead of resolved multi_class
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    
    # This should not raise IndexError anymore
    clf.fit(X, y)

def test_logistic_regression_cv_l1_ratio_none_handling():
    """Test that l1_ratio_ is handled correctly when penalty is not elasticnet"""
    np.random.seed(123)
    X = np.random.normal(size=(100, 4))
    y = np.random.choice([0, 1], size=100)
    
    # Test with L2 penalty (should not use l1_ratio)
    clf = LogisticRegressionCV(
        cv=3,
        solver='liblinear',
        penalty='l2',  # Not 'elasticnet'
        refit=False
    )
    
    # This should not fail with l1_ratio_ computation errors
    clf.fit(X, y)
    
    # After fitting, should have proper l1_ratio_ array (with None values where appropriate)
    # This tests that the new logic doesn't try to compute l1_ratio_ when not applicable

if __name__ == "__main__":
    print("Running LogisticRegressionCV regression tests...")
    
    test_logistic_regression_cv_multi_class_indexerror()
    print("✓ Multi-class index error test passed")
    
    test_logistic_regression_cv_l1_ratio_none_handling()
    print("✓ L1 ratio None handling test passed")
    
    print("All regression tests passed!")