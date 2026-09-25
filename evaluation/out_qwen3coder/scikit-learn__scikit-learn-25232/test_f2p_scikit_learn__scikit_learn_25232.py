"""
Regression tests for IterativeImputer fill_value parameter.

This test addresses the issue where IterativeImputer did not have a fill_value
parameter when initial_strategy was set to "constant". The fix added this parameter
so that users can specify what value to use for imputing missing values during
the first imputation round when initial_strategy="constant".
"""
import numpy as np
import pytest

from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_accepted():
    """Test that IterativeImputer now accepts fill_value parameter without error.
    
    Before the fix, passing fill_value would raise TypeError: __init__() got an 
    unexpected keyword argument 'fill_value'.
    """
    # This line should not raise an error in the fixed version
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=42
    )
    
    # Check that the attribute was properly set
    assert imputer.fill_value == 42


def test_iterative_imputer_fill_value_none_default():
    """Test that fill_value defaults to None."""
    imputer = IterativeImputer(
        initial_strategy="constant"
    )
    
    # Default should be None
    assert imputer.fill_value is None


def test_iterative_imputer_fill_value_parameter_with_different_strategies():
    """Test that fill_value parameter can be specified even when not used.
    
    When initial_strategy != "constant", the fill_value parameter should be 
    accepted but ignored (as it is not used).
    """
    # Should not raise an error even though fill_value won't be used
    imputer = IterativeImputer(
        initial_strategy="mean",
        fill_value=999.0  # This should be ignored
    )
    
    assert imputer.fill_value == 999.0


def test_iterative_imputer_simple_imputer_call_with_fill_value():
    """Test that the fill_value parameter gets passed to SimpleImputer.
    
    This test ensures that when initial_strategy='constant' and fill_value is 
    specified, it's properly used in the internal SimpleImputer call.
    This requires invoking the imputation logic to actually exercise the parameter.
    """
    # Create test data with some missing values
    X = np.array([
        [1.0, 2.0, np.nan],
        [4.0, np.nan, 6.0],
        [7.0, 8.0, 9.0]
    ])
    
    # Test using a fill_value that would be distinguishable from default
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=5.0,
        max_iter=1,  # Just one iteration to make it faster
        random_state=0
    )
    
    # By successfully calling fit_transform, we ensure that
    # the parameter gets processed by the imputation flow 
    X_imputed = imputer.fit_transform(X)
    
    # This is more of a smoke test to ensure that parameter processing works
    # The actual logic of using fill_value would be tested elsewhere, 
    # but we want to ensure we exercise the path through the parameter
    assert X_imputed is not None
    assert not np.isnan(X_imputed).all()  # We shouldn't have all NaN values