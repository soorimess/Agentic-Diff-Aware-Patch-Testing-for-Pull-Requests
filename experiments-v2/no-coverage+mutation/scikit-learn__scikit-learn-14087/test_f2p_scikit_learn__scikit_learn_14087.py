"""
Regression test for IndexError with LogisticRegressionCV and refit=False.

This test reproduces the bug where LogisticRegressionCV with refit=False
throws an IndexError when using certain solvers.
"""
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV
from sklearn.utils.estimator_checks import check_estimator


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError."""
    # This is the exact reproduction case from the bug report
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
    
    # This should not raise IndexError
    clf.fit(X, y)
    
    # Verify that the estimator has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_multinomial():
    """Test LogisticRegressionCV with refit=False and multinomial multi_class."""
    np.random.seed(29)
    X = np.random.normal(size=(100, 4))
    y = np.random.randint(0, 3, size=100)  # 3 classes
    
    # Test with multinomial multi_class
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='multinomial'
    )
    
    # This should not raise IndexError
    clf.fit(X, y)
    
    # Verify that the estimator has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


if __name__ == "__main__":
    # Run the tests
    test_logistic_regression_cv_refit_false_indexerror()
    test_logistic_regression_cv_refit_false_multinomial()
    print("All tests passed!")