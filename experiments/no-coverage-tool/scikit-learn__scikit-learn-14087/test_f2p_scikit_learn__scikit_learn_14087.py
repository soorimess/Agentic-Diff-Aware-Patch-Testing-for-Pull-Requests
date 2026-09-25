"""
Regression test for IndexError with LogisticRegressionCV and refit=False
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_no_indexerror_refit_false():
    """Test that LogisticRegressionCV with refit=False does not raise IndexError.
    
    This reproduces the exact bug reported: IndexError thrown with 
    LogisticRegressionCV and refit=False.
    """
    # Reproduce exact test case from bug report 
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should not raise IndexError
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This line was throwing: IndexError: too many indices for array
    clf.fit(X, y)
    
    # If we get here, no IndexError was raised
    assert len(clf.C_) > 0