"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test ensures that the bug where LogisticRegressionCV with refit=False
throws an IndexError is properly fixed.
"""

import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError.
    
    This is a regression test for the bug where LogisticRegressionCV with 
    refit=False would raise an IndexError when using certain solvers and 
    multi_class configurations.
    """
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
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_multinomial():
    """Test LogisticRegressionCV with refit=False and multinomial multi_class."""
    np.random.seed(29)
    X = np.random.normal(size=(100, 4))
    y = np.random.randint(0, 3, size=100)
    
    # Test with multinomial multi_class
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        multi_class='multinomial',
        tol=1e-2,
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_refit_false_l1_ratio_handling():
    """Test proper l1_ratio handling for non-elasticnet penalty.
    
    This tests that when penalty is not elasticnet, None is appended to l1_ratio_.
    """
    np.random.seed(29)
    X = np.random.normal(size=(50, 3))  # Smaller dataset to avoid convergence issues
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Test with l2 penalty (not elasticnet) - should append None to l1_ratio_
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        penalty='l2',  # not elasticnet
        tol=1e-2,
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model has the expected attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    # For non-elasticnet penalty, l1_ratio_ should contain None values
    assert len(clf.l1_ratio_) > 0
    # All l1_ratios should be None for l2 penalty
    assert all(r is None for r in clf.l1_ratio_)


if __name__ == "__main__":
    # Run the tests manually for debugging
    test_logistic_regression_cv_refit_false_indexerror()
    print("Test 1 passed")
    test_logistic_regression_cv_refit_false_multinomial()
    print("Test 2 passed")
    test_logistic_regression_cv_refit_false_l1_ratio_handling()
    print("Test 3 passed")