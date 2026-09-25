"""
Regression test for IndexError with LogisticRegressionCV and refit=False

This test ensures that LogisticRegressionCV works correctly with refit=False
and does not raise an IndexError when multi_class is 'ovr' or handles the
specific indexing bug in the original code.
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """
    Test for IndexError when using LogisticRegressionCV with refit=False.
    
    This specifically addresses the bug where using LogisticRegressionCV with 
    solver='saga', refit=False would result in:
    IndexError: too many indices for array: array is 3-dimensional, but 4 were indexed
    
    The bug was in the indexing logic when multi_class != 'ovr'.
    """
    # Set up test data as in the bug report
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
    
    # The most critical assertion - no IndexError should be raised
    clf.fit(X, y)
    
    # Verify successful completion
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0


def test_logistic_regression_cv_refit_false_multinomial():
    """
    Test that multinomial case works with refit=False.
    
    This ensures the fix handles multi-class scenarios correctly.
    """
    # Set up test data (multiclass)
    np.random.seed(42)
    X = np.random.normal(size=(100, 4))
    y = np.random.randint(0, 3, size=100)  # 3 classes
    
    # Test multinomial case
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        multi_class='multinomial',
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify successful completion
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0


def test_logistic_regression_cv_refit_false_elasticnet():
    """
    Test that elasticnet penalty works with refit=False.
    
    This is to ensure the l1_ratio_ logic also works correctly when penalty='elasticnet'.
    """
    # Set up test data
    np.random.seed(29)
    X = np.random.normal(size=(100, 4))  # smaller dataset for efficiency 
    beta = np.random.normal(size=4)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Test with elasticnet penalty to cover l1_ratio handling code paths
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9],  # This triggers the conditional path
        refit=False
    )
    
    # This should not crash (and specifically should not crash on l1_ratio_ handling)
    clf.fit(X, y)
    
    # Verify successful completion
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) > 0
    # With elasticnet, l1_ratio_ should contain either None or numeric values
    assert len(clf.l1_ratio_) > 0


if __name__ == "__main__":
    test_logistic_regression_cv_refit_false_indexerror()
    test_logistic_regression_cv_refit_false_multinomial()
    test_logistic_regression_cv_refit_false_elasticnet()
    print("All tests passed!")