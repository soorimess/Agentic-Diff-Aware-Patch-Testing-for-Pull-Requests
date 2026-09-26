"""Test for the specific bug in LogisticRegressionCV with refit=False.

This test reproduces the IndexError that occurs when using LogisticRegressionCV
with refit=False and penalty != 'elasticnet'.
"""

import numpy as np
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_no_indexerror():
    """Test that LogisticRegressionCV with refit=False works without IndexError."""
    # Set up the test data as in the bug report
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
    
    # This line should not raise IndexError: too many indices for array
    clf.fit(X, y)
    
    # Verify that the model was fitted properly
    assert hasattr(clf, 'C_')
    assert hasattr(clf, 'l1_ratio_')
    assert len(clf.C_) == 1
    assert clf.l1_ratio_[0] is None  # Should be None when penalty != 'elasticnet'