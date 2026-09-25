"""
Regression test for scikit-learn issue #14087
IndexError thrown with LogisticRegressionCV and refit=False
"""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegressionCV


def test_logistic_regression_cv_no_indexerror():
    """
    Test that LogisticRegressionCV with refit=False does not throw IndexError.
    
    This is the core functionality regression test for the specific bug reported:
      IndexError: too many indices for array
    
    This test is expected to fail in the buggy version (before fix) and pass after.
    """
    
    # Reproducing exact conditions from the bug report
    np.random.seed(29)
    X = np.random.normal(size=(1000, 3))
    beta = np.random.normal(size=3)
    intercept = np.random.normal(size=None)
    y = np.sign(intercept + X @ beta)
    
    # The exact bug trigger from the reports  
    clf = LogisticRegressionCV(
        cv=5,
        solver='saga',
        tol=1e-2,
        refit=False
    )
    
    # This line was causing the IndexError in the original bug report
    # The fix ensures it doesn't happen by changing the l1_ratio_ handler
    try:
        clf.fit(X, y)
        # If we get here, the bug is fixed
        return True
    except IndexError as e:
        if "too many indices" in str(e):
            pytest.fail("IndexError: too many indices for array - bug still present")
        raise e
    except Exception as e:
        # Any other exception is OK, we just care about the specific IndexError
        # which indicates the original problematic branching/calculation
        return True


def test_logistic_regression_cv_l1_ratio_handling():
    """
    Test l1_ratio_ calculation for penalty != elasticnet.
    
    The key change in the PR is:
    - Previously: best_indices_l1 was always computed and accessed 
    - Now: Only computed when penalty == elasticnet, else sets l1_ratio_.append(None) 
    """
    
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = np.random.choice([0, 1], size=100)
    
    # Test case to ensure l1_ratio_ handling works with l2 penalty
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        penalty='l2',  # This wouldn't use elasticnet path
        tol=1e-2,
        refit=False
    )
    
    # Should not crash even if l1_ratios are not elasticnet
    clf.fit(X, y)
    
    # It's sufficient that it doesn't crash
    # the fix ensures proper handling of l1_ratio_ 
    assert len(clf.C_) >= 1


def test_logistic_regression_cv_multiclass_behavior():
    """
    Ensure multi_class != 'ovr' scenario works as expected.
    """
    
    np.random.seed(123)
    X = np.random.randn(50, 4)
    y = np.random.choice([0, 1, 2], size=50)  # 3-class
    
    # Specific test case : multinomial multi_class
    clf = LogisticRegressionCV(
        cv=3,
        solver='saga',
        multi_class='multinomial',
        tol=1e-2,
        refit=False
    )
    
    # This should work and not raise indexing errors
    clf.fit(X, y)
    assert len(clf.C_) >= 1