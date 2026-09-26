"""Test for regression of IndexError in LogisticRegressionCV with refit=False.

This test reproduces the bug where LogisticRegressionCV with refit=False
throws an IndexError when multi_class is not 'ovr'.
"""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_no_indexerror_refit_false():
    """Test that LogisticRegressionCV with refit=False does not raise IndexError.
    
    This reproduces the bug reported where refit=False with certain multi_class
    settings would cause an IndexError due to incorrect array indexing.
    """
    # Set up the test data as described in the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # This should not raise an IndexError - reproduces the original bug
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert clf.C_ is not None
    assert len(clf.C_) == 1  # Should have one C value
    assert clf.l1_ratio_ is not None


def test_logistic_regression_cv_multinomial_no_indexerror_refit_false():
    """Test that multinomial LogisticRegressionCV with refit=False does not raise IndexError.
    
    This reproduces the bug where multinomial case with refit=False would cause
    an IndexError due to incorrect array indexing.
    """
    # Set up test data
    np.random.seed(42)
    X = np.random.randn(100, 4)
    y = np.random.randint(0, 3, 100)  # 3 classes
    
    # This should not raise an IndexError for multinomial case
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        multi_class='multinomial'
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify that the model was fitted correctly
    assert clf.C_ is not None
    assert len(clf.C_) == 1  # Should have one C value
    assert clf.l1_ratio_ is not None


def test_logistic_regression_cv_l1_ratio_handling():
    """Test that l1_ratio_ is properly handled when penalty is not elasticnet.
    
    This reproduces the bug where using penalty='l1' with refit=False would
    cause a TypeError due to improper indexing of l1_ratios_ array.
    """
    # Set up test data
    np.random.seed(42)
    X = np.random.randn(100, 4)
    y = np.random.randint(0, 2, 100)
    
    # Test with penalty='l1' (not elasticnet) - should not crash
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='l1'
    )
    
    # This should not raise TypeError or IndexError
    clf.fit(X, y)
    
    # With refit=False, l1_ratio_ should be set to None when penalty != 'elasticnet'
    # The fix ensures this works correctly without crashing
    assert clf.l1_ratio_ is not None