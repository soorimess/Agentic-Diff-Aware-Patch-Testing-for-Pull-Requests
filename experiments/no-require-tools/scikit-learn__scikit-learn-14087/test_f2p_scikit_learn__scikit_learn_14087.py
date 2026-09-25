"""
Regression tests for LogisticRegressionCV bug with refit=False.
Issue: IndexError with LogisticRegressionCV and refit=False
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_main_bug():
    """Test the main bug reported: IndexError with LogisticRegressionCV and refit=False.
    
    Original bug report: IndexError thrown with LogisticRegressionCV and refit=False
    Error: IndexError: too many indices for array
    """
    # Exact reproduction as in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # This used to raise IndexError: too many indices for array
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    
    # This should not raise IndexError anymore
    clf.fit(X, y)
    
    # Verify successful completion with expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_with_elasticnet():
    """Test that elasticnet penalty works with refit=False (tests the else branch).
    
    Tests the l1_ratio_ logic path that was part of the fix.
    """
    # Similar setup but uses elasticnet penalty which hits different path
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Use elasticnet penalty - should have different l1_ratio_ handling
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9],
        refit=False
    )
    
    # This should not raise errors
    clf.fit(X, y)
    
    # Verify successful completion
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    # With elasticnet penalty, l1_ratio_ should have numerical values, not None
    if len(clf.l1_ratio_) > 0:
        assert all(r is not None for r in clf.l1_ratio_)


if __name__ == "__main__":
    # Run the tests manually
    test_logistic_regression_cv_refit_false_main_bug()
    print("SUCCESS: Main bug test passed - no IndexError when refit=False")
    
    test_logistic_regression_cv_refit_false_with_elasticnet()
    print("SUCCESS: Elasticnet test passed - l1_ratio_ handling works")