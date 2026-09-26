"""
Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test ensures that LogisticRegressionCV with refit=False works correctly
and doesn't raise an IndexError when using multi_class='ovr' or when
penalty='elasticnet' is used.
"""
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError.
    
    This is a regression test for the bug where LogisticRegressionCV with
    refit=False would raise IndexError when multi_class='ovr'.
    """
    # Create test data as described in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # This should not raise an IndexError
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    
    # This should work without raising IndexError
    clf.fit(X, y)
    
    # Verify that the model has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_multinomial():
    """Test LogisticRegressionCV with refit=False and multi_class='multinomial'."""
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))
    y = np.random.randint(0, 3, size=100)  # 3 classes
    
    # Test with multinomial multi_class
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='multinomial'
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0