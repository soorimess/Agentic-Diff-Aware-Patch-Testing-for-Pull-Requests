"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This file contains tests for the bug reported in issue #14087 where
LogisticRegressionCV with refit=False raised an IndexError under certain
conditions. The specific behaviors that were fixed are:
1. Using correct 'multi_class' variable instead of 'self.multi_class' for indexing
2. Proper handling of l1_ratio_ for different penalty types
"""

import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_indexerror_with_refit_false():
    """Test that LogisticRegressionCV with refit=False works without IndexError.
    
    This tests the core bug that was fixed: using self.multi_class instead of 
    the computed local multi_class variable, causing wrong array indexing.
    
    The specific error: IndexError: too many indices for array - array is 3-dimensional
    but 4 were indexed - was caused by incorrect logic branching due to wrong variable.
    """
    # Use the exact test case from the bug report that was failing
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This would fail with IndexError before the fix
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False)
    
    # Should not raise IndexError after the fix
    clf.fit(X, y)
    
    # Verify basic functionality was preserved
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_l1_ratio_none_handling():
    """Test proper handling of l1_ratio_ for non-elasticnet penalties.
    
    This tests that when penalty != 'elasticnet', l1_ratio_.append(None) is called
    rather than trying to compute means, as was fixed in the patch.
    """
    # Test with a non-elasticnet penalty (default l2)  
    np.random.seed(123)
    X = np.random.normal(size=(150, 4))
    beta = np.random.normal(size=4)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with l2 penalty (default) - should set l1_ratio_ to None values 
    clf = LogisticRegressionCV(
        cv=4,
        solver='saga',
        tol=1e-2,
        penalty='l2',  # Non-elasticnet penalty
        refit=False)
    
    # Should not raise TypeError or IndexError after the fix
    clf.fit(X, y)
    
    # Verify l1_ratio_ is set appropriately for non-elasticnet case
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0
    # For non-elasticnet penalty, l1_ratio_ should be None
    assert all(r is None for r in clf.l1_ratio_)


if __name__ == "__main__":
    # Run the tests directly
    test_logistic_regression_cv_indexerror_with_refit_false()
    test_logistic_regression_cv_l1_ratio_none_handling()
    print("All tests passed!")