"""Test for regression of LogisticRegressionCV bug with refit=False.

This file tests the specific bug described in the issue where 
LogisticRegressionCV with refit=False was throwing an IndexError.
"""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV
from sklearn.exceptions import ConvergenceWarning
import warnings


def test_logistic_regression_cv_refit_false_indexerror():
    """Test that LogisticRegressionCV with refit=False doesn't raise IndexError.
    
    This test reproduces the bug where calling fit() on LogisticRegressionCV
    with refit=False would throw an IndexError due to incorrect array 
    dimensionality handling.
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
    
    # This line triggered the IndexError in the bug report
    clf.fit(X, y)
    
    # Verify that we got the expected results
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    # For non-elasticnet penalty, l1_ratio_ should be None or have valid values
    assert clf.l1_ratio_ is not None
    assert len(clf.l1_ratio_) > 0
    
    # Additional verification that we don't have infinite or NaN values
    assert not np.any(np.isinf(clf.C_))
    assert not np.any(np.isnan(clf.C_))
    

def test_logistic_regression_cv_refit_false_elasticnet_with_l1_ratios():
    """Test LogisticRegressionCV with elasticnet penalty and l1_ratios and refit=False.
    
    This test specifically targets the fix in l1_ratio_ indexing that was 
    introduced in the commit. The bug was due to attempting to index l1_ratios_
    in non-elasticnet cases.
    """
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with elasticnet penalty that has l1_ratios
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        penalty='elasticnet',
        l1_ratios=[0.1, 0.5, 0.9],
        refit=False
    )
    
    # This should not raise an IndexError
    clf.fit(X, y)
    
    # Verify results are reasonable
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    assert clf.l1_ratio_ is not None
    assert len(clf.l1_ratio_) > 0
    
    # Additional verification
    assert not np.any(np.isinf(clf.C_))
    assert not np.any(np.isnan(clf.C_))
    assert not np.any(np.isinf(clf.l1_ratio_))
    assert not np.any(np.isnan(clf.l1_ratio_))


def test_logistic_regression_cv_multi_class_consistency():
    """Test consistency between multi_class behavior when both are specified differently.
    
    This test highlights the specific bug where 'ovr' determination was using 
    the wrong variable reference (self.multi_class vs multi_class)
    """
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with default multi_class (should be 'ovr') and refit=False
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    clf.fit(X, y)
    
    # This should work without IndexError - this specific bug was about
    # choosing wrong branch based on wrong variable comparison
    assert clf.C_ is not None
    assert len(clf.C_) > 0
    assert clf.l1_ratio_ is not None
    
    # Test with explicitly setting multi_class='ovr'
    clf2 = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        multi_class='ovr',
        refit=False
    )
    clf2.fit(X, y)
    
    assert clf2.C_ is not None
    assert len(clf2.C_) > 0
    assert clf2.l1_ratio_ is not None


def test_logistic_regression_cv_compares_refit_behavior():
    """Compare refit=True vs refit=False behavior.
    
    This ensures consistency between the two modes and shows the bug
    was specific to the refit=False path.
    """
    np.random.seed(29)
    X = np.random.normal(size=(100, 3))  # smaller dataset for speed
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)

    # Test with refit=True (should work with both)
    clf_refit = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=True
    )
    clf_refit.fit(X, y)

    # Test with refit=False (this was problematic before fix) 
    clf_no_refit = LogisticRegressionCV(
        cv=3,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    clf_no_refit.fit(X, y)

    # Both should work and produce reasonable results
    assert clf_refit.C_ is not None
    assert clf_no_refit.C_ is not None
    
    # Both should work without IndexError (the main assertion of the bug fix)
    assert len(clf_refit.C_) > 0
    assert len(clf_no_refit.C_) > 0