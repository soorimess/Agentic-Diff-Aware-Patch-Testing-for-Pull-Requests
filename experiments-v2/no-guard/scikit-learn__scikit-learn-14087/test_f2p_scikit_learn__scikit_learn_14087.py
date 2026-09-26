"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test reproduces the bug where LogisticRegressionCV with refit=False
and penalty != 'elasticnet' would throw an IndexError due to accessing
out-of-bounds indices in l1_ratios_ array.
"""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError.
    
    This reproduces the exact bug reported where using refit=False with 
    solver='saga' and default penalty would cause an IndexError.
    """
    # Set up test data as in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Test with the exact parameters from the bug report
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This should not raise an IndexError (this was the original bug)
    clf.fit(X, y)
    
    # Verify basic properties are set correctly
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    assert clf.coef_ is not None
    assert len(clf.coef_) > 0


def test_logistic_regression_cv_refit_false_l2_penalty():
    """Test that LogisticRegressionCV with refit=False and l2 penalty works.
    
    This tests the specific case that was broken when penalty != 'elasticnet'.
    """
    # Set up test data
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # Test with l2 penalty and refit=False (the main bug case)
    clf = LogisticRegressionCV(
        cv=3,
        penalty='l2',  # This is the key - not 'elasticnet'
        solver='liblinear',
        tol=1e-2,
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify the model was fitted correctly
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    assert clf.coef_ is not None
    assert len(clf.coef_) > 0
    # For l2 penalty, l1_ratio_ should be None or have None values
    if clf.l1_ratio_ is not None:
        assert len(clf.l1_ratio_) > 0
        # All values should be None for l2 penalty (the fix handles this)
        for ratio in clf.l1_ratio_:
            assert ratio is None or ratio == 0.0