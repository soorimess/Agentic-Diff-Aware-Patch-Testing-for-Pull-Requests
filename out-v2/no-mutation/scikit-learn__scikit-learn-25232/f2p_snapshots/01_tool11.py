"""
Test for IterativeImputer fill_value parameter.

This test verifies that IterativeImputer accepts a fill_value parameter
when initial_strategy='constant', which allows users to specify custom
values for imputing missing data.
"""

import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter without error."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work after the fix - using fill_value with initial_strategy='constant'
    imputer = IterativeImputer(
        initial_strategy='constant',
        fill_value=999.0,
        random_state=0
    )
    
    # This should not raise an error
    X_imputed = imputer.fit_transform(X)
    
    # Should return valid array without error
    assert X_imputed is not None
    assert X_imputed.shape == X.shape


def test_iterative_imputer_fill_value_none_default():
    """Test that IterativeImputer accepts fill_value=None."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work with default fill_value=None
    imputer = IterativeImputer(
        initial_strategy='constant',
        fill_value=None,
        random_state=0
    )
    
    # This should not raise an error
    X_imputed = imputer.fit_transform(X)
    
    # Should return valid array without error
    assert X_imputed is not None
    assert X_imputed.shape == X.shape


def test_iterative_imputer_fill_value_with_nan():
    """Test that IterativeImputer accepts np.nan as fill_value."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work after the fix - using np.nan as fill_value
    imputer = IterativeImputer(
        initial_strategy='constant',
        fill_value=np.nan,
        random_state=0
    )
    
    # This should not raise an error
    X_imputed = imputer.fit_transform(X)
    
    # Should return valid array without error
    assert X_imputed is not None
    assert X_imputed.shape == X.shape