"""
Test for LogisticRegressionCV IndexError when refit=False
Bug report: IndexError thrown with LogisticRegressionCV and refit=False
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_basic():
    """
    Test the basic case from bug report that was causing IndexError.
    The first fix was: using local variable 'multi_class' instead of 'self.multi_class'
    in the multi_class condition check.
    """
    # Test the exact case that was failing in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should not raise an IndexError according to the bug report (when fixed properly)
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This was the main bug location: IndexError about too many indices for array
    # In original code, wrong condition check caused wrong indexing 
    clf.fit(X, y)
    
    # Verify fit works and returns proper output structure
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert len(clf.l1_ratio_) == 1


def test_logistic_regression_cv_refit_false_multinomial():
    """
    Test multinomial case with refit=False - exercises the indexing fix correctly.
    This is where the indexing was wrong in the original buggy code.
    """
    # Test: should work with multinomial multi_class but was breaking 
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='multinomial'  # Different from default 'ovr'
    )
    
    # This test specifically verifies the indexing fix 
    # The error was: IndexError: too many indices for array: array is 3-dimensional, but 4 were indexed
    clf.fit(X, y)
    
    # Verify that fit succeeded
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert len(clf.l1_ratio_) == 1


def test_logistic_regression_cv_refit_false_ovr():
    """
    Test OVR case explicitly - ensures the fix doesn't break the working case.
    """
    # Test: OVR case that was already working before the fix
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='ovr'
    )
    
    # This should have worked both before and after the fix
    clf.fit(X, y)
    
    # Verify that fit succeeded  
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert len(clf.l1_ratio_) == 1


def test_logistic_regression_cv_refit_false_elasticnet():
    """
    Test elasticnet penalty case that exercises the l1_ratio_ handling fix.
    This tests the second fix: proper handling of l1_ratio_ when penalty != 'elasticnet'.
    """
    # Test elasticnet case which needed l1_ratios_ to be properly handled
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # For elasticnet, we must provide l1_ratios
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9],  # Required for elasticnet
        tol=1e-2,
        refit=False
    )
    
    # This tests the exact l1_ratio_ handling from the diff fix on lines 2183-2185
    clf.fit(X, y)
    
    # Verify that fit succeeded and has proper attributes
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert len(clf.l1_ratio_) == 1


if __name__ == "__main__":
    test_logistic_regression_cv_refit_false_basic()
    test_logistic_regression_cv_refit_false_multinomial() 
    test_logistic_regression_cv_refit_false_ovr()
    test_logistic_regression_cv_refit_false_elasticnet()
    print("All tests passed!")