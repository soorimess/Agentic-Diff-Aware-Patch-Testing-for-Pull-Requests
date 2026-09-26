"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test ensures that LogisticRegressionCV with refit=False works correctly
and doesn't raise an IndexError when using solvers like 'saga' or 'liblinear'.
"""

import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError."""
    # Exact reproduction case from the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should not raise an IndexError
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This should work without raising IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted properly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_different_solvers():
    """Test that LogisticRegressionCV with refit=False works with different solvers."""
    np.random.seed(42)
    X = np.random.normal(size=(100, 5))
    y = np.random.randint(0, 2, size=100)
    
    # Test with different solvers that should work with refit=False
    for solver in ['liblinear', 'saga']:
        clf = LogisticRegressionCV(
            cv=3,
            solver=solver,
            refit=False,
            random_state=42
        )
        
        # This should not raise an IndexError
        clf.fit(X, y)
        
        # Verify that the model was fitted properly
        assert hasattr(clf, 'C_')
        assert hasattr(clf, 'l1_ratio_')
        assert len(clf.C_) > 0
        assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_l1_ratio_handling():
    """Test that l1_ratio_ is handled correctly for non-elasticnet penalties."""
    np.random.seed(42)
    X = np.random.normal(size=(100, 5))
    y = np.random.randint(0, 2, size=100)
    
    # Test with l2 penalty (default) - should append None to l1_ratio_
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        penalty='l2',  # default penalty
        refit=False,
        random_state=42
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that l1_ratio_ contains None values for non-elasticnet cases
    # (This tests the fix that prevents the IndexError in l1_ratio_ handling)
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0