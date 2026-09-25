"""
Test for LogisticRegressionCV with refit=False
This specifically tests the exact IndexError described in the bug report
and related l1_ratio handling bugs.
"""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """
    Test for the core bug reported: IndexError with LogisticRegressionCV and refit=False.
    
    This is the exact code from the bug report that should not raise an IndexError.
    """
    # Setup code from the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should work without throwing IndexError: too many indices for array
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This line should not raise IndexError in the OLD buggy code
    # but should work fine in the fixed version
    clf.fit(X, y)
    
    # Basic validation that fitting worked
    assert clf.C_ is not None
    assert len(clf.C_) > 0


def test_logistic_regression_cv_refit_false_overr():
    """
    Test with explicit multi_class='ovr' which was mentioned as one case that failed.
    """
    # Setup code from the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test explicitly with multi_class='ovr'
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='ovr'
    )
    
    # This line should not raise IndexError
    clf.fit(X, y)
    
    # Basic validation that fitting worked
    assert clf.C_ is not None
    assert len(clf.C_) > 0


def test_logistic_regression_cv_refit_false_elasticnet_penalty():
    """
    Test with elasticnet penalty to ensure proper l1_ratio handling.
    This tests the fix for l1_ratio indexing with non-elasticnet penalties.
    """
    # Setup test data
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with elasticnet penalty - this should work without errors
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9],
        multi_class='ovr'
    )
    
    # This should not raise a TypeError when handling l1_ratio_ indexing
    clf.fit(X, y)
    
    # Basic validation that fitting worked
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    assert clf.l1_ratio_ is not None
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_default_penalty():
    """
    Test with default penalty to ensure proper l1_ratio handling for non-elasticnet cases.
    """
    # Setup test data
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with default penalty (should be 'l2') - this should work without errors
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='ovr'
    )
    
    # This should not raise a TypeError (the other bug that was fixed)
    clf.fit(X, y)
    
    # Basic validation that fitting worked
    assert clf.C_ is not None
    assert len(clf.C_) > 0


if __name__ == "__main__":
    # Run the tests 
    test_logistic_regression_cv_refit_false_indexerror()
    test_logistic_regression_cv_refit_false_overr()
    test_logistic_regression_cv_refit_false_elasticnet_penalty()
    test_logistic_regression_cv_refit_false_default_penalty()
    print("All tests completed successfully!")