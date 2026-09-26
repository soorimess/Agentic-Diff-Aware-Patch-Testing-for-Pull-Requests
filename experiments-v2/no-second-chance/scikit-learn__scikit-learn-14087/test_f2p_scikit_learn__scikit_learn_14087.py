"""
Test for the bug in LogisticRegressionCV with refit=False.

This test reproduces the IndexError that occurs when using 
LogisticRegressionCV with refit=False and multi_class='ovr'.
"""
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """
    Test that reproduces the exact IndexError from the bug report.
    
    The bug occurs when:
    - refit=False
    - multi_class='ovr' (default) 
    - The indexing logic was wrong due to condition check issue
    """
    # Set up the test data exactly as in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # This exact code from the bug report should not raise IndexError
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This should not raise IndexError: too many indices for array
    # The bug was that with refit=False, multi_class='ovr', and certain
    # conditions, the wrong indexing path was taken causing the error
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1  # Should have one C value
    assert len(clf.l1_ratio_) == 1  # Should have one l1_ratio value


def test_logistic_regression_cv_refit_false_multinomial():
    """
    Test that LogisticRegressionCV with refit=False works with multinomial.
    """
    # Set up test data with multiple classes
    np.random.seed(29)
    X = np.random.normal(size=(100, 4))
    y = np.random.randint(0, 3, size=100)  # 3 classes
    
    # Test with multinomial
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='multinomial'
    )
    
    # This should not raise IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 3  # Should have one C value per class
    assert len(clf.l1_ratio_) == 3  # Should have one l1_ratio value per class


def test_logistic_regression_cv_refit_false_l2_penalty():
    """
    Test that LogisticRegressionCV with refit=False works with l2 penalty.
    """
    # Set up test data
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Test with l2 penalty (no elasticnet)
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='l2'  # No elasticnet
    )
    
    # This should not raise any errors
    clf.fit(X, y)
    
    # With l2 penalty, l1_ratio_ should be None
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert clf.l1_ratio_[0] is None  # Should be None for l2 penalty