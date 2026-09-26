import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """
    Test for IndexError with LogisticRegressionCV and refit=False.
    
    This test reproduces the bug reported where LogisticRegressionCV with 
    refit=False raises IndexError when using certain parameter combinations.
    """
    # Reproduce the exact case from the bug report
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
        refit=False)
    
    # This line should not raise IndexError: too many indices for array
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert hasattr(clf, 'coef_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


def test_logistic_regression_cv_elasticnet_refit_false():
    """
    Test for proper handling of elasticnet penalty with refit=False.
    
    This test ensures that the fix for the l1_ratio_ indexing works correctly.
    """
    # Test with elasticnet penalty which triggers the 4D array case
    np.random.seed(42)
    X = np.random.normal(size=(100, 4))
    y = np.random.randint(0, 3, size=100)  # 3 classes
    
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9])
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert hasattr(clf, 'coef_')
    assert len(clf.C_) > 0
    assert len(clf.l1_ratio_) > 0


if __name__ == "__main__":
    test_logistic_regression_cv_refit_false_indexerror()
    print("First test passed!")
    test_logistic_regression_cv_elasticnet_refit_false()
    print("Second test passed!")