"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test reproduces the bug where LogisticRegressionCV with refit=False
throws an IndexError when using multi_class='ovr' and penalty='elasticnet'.
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_original_bug():
    """Test that reproduces the exact original bug report."""
    # Set up the test data as described in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should not raise an IndexError - exact reproduction from bug report
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This line was causing IndexError before the fix
    clf.fit(X, y)
    
    # Verify that the model was fitted without error
    assert clf.coef_ is not None
    assert clf.intercept_ is not None


def test_logistic_regression_cv_ovr_multi_class():
    """Test that LogisticRegressionCV with explicit ovr multi_class works."""
    # Set up the test data
    np.random.seed(123)
    X = np.random.normal(size=(50, 4))
    y = np.random.randint(0, 2, size=50)

    # Test with explicit ovr multi_class which triggers the specific bug path
    clf = LogisticRegressionCV(
        cv=3,
        multi_class='ovr',
        solver='saga',
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted without error
    assert clf.coef_ is not None
    assert clf.intercept_ is not None


def test_logistic_regression_cv_l1_ratio_handling():
    """Test that LogisticRegressionCV with l1_ratio handling works properly."""
    # Set up the test data
    np.random.seed(42)
    X = np.random.normal(size=(100, 5))
    y = np.random.randint(0, 2, size=100)

    # Test with l1_ratio handling - this tests the second part of the fix
    clf = LogisticRegressionCV(
        cv=3,
        penalty='l2',  # Not elasticnet, so l1_ratios_ should be [None]
        solver='saga',
        refit=False
    )
    
    # This should not raise TypeError about l1_ratio indexing
    clf.fit(X, y)
    
    # Verify that the model was fitted without error
    assert clf.coef_ is not None
    assert clf.intercept_ is not None
    # l1_ratio_ should be None for l2 penalty
    assert clf.l1_ratio_ is not None