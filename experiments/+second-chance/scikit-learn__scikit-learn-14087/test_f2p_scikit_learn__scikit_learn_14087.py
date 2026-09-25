"""
Test to reproduce the IndexError bug in LogisticRegressionCV with refit=False.
This test is designed to capture the exact conditions that were causing the IndexError.
"""
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_indexerror_refit_false():
    """Test that demonstrates the IndexError that was fixed.
    
    The original bug was that when refit=False, with certain multi_class settings,
    an IndexError would be thrown due to incorrect multi_class condition comparison.
    """
    # Exact reproduction case from the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # This should not raise an IndexError after the fix
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',  # same error with 'liblinear'
        tol=1e-2,
        refit=False
    )
    
    # This should succeed (this was the main bug that was reported)
    clf.fit(X, y)
    
    # Verify we got the expected shape results
    assert len(clf.C_) == 1  # For binary classification 
    assert len(clf.l1_ratio_) == 1
    assert clf.l1_ratio_[0] is None  # Should be None when not using elasticnet


def test_logistic_regression_cv_l1_ratio_none_when_not_elasticnet():
    """
    Test that l1_ratio_ is None when penalty is not 'elasticnet' and refit=False.
    
    This covers the second part of the pull request fix - ensuring that
    l1_ratio_ properly handles non-elasticnet penalties.
    """
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with penalty='l2' (not elasticnet) - simple case 
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='l2'
    )
    
    clf.fit(X, y)
    
    # With penalty='l2', l1_ratio_ should be [None] 
    # This is the behavior that was fixed
    assert clf.l1_ratio_ == [None]


def test_logistic_regression_cv_l1_ratio_with_elasticnet():
    """
    Test that l1_ratio_ works properly when penalty is 'elasticnet' and refit=False.
    
    This tests the elasticnet branch that handles the proper l1_ratio_ computation.
    """
    np.random.seed(29)
    X = np.random.normal(size=(50, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with penalty='elasticnet' 
    clf = LogisticRegressionCV(
        cv=2,
        solver='saga',
        tol=1e-2,
        refit=False,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5]
    )
    
    clf.fit(X, y)
    
    # With penalty='elasticnet', l1_ratio_ should be a proper averaged value, not None
    # This exercises the lines that compute best_indices_l1 for elasticnet
    assert clf.l1_ratio_[0] is not None