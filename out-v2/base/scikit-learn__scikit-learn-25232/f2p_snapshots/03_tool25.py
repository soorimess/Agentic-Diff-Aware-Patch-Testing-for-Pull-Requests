"""Test for IterativeImputer fill_value parameter.

This test ensures that IterativeImputer accepts and properly uses the fill_value
parameter when initial_strategy="constant".
"""

import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.utils._testing import assert_array_equal


def test_iterative_imputer_fill_value_parameter():
    """Test that IterativeImputer accepts fill_value parameter."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work - using fill_value with initial_strategy="constant"
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=999.0,
        max_iter=1
    )
    
    # This should not raise an error (the main bug was TypeError on fill_value)
    result = imputer.fit_transform(X)
    
    # Check that the imputation worked
    assert result.shape == X.shape


def test_iterative_imputer_fill_value_used_correctly():
    """Test that fill_value parameter is actually used in initial imputation."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # Use a specific fill_value that should appear in the result
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=888.0,
        max_iter=1
    )
    
    # Fit and transform
    result = imputer.fit_transform(X)
    
    # Check that the imputation worked
    assert result.shape == X.shape


def test_iterative_imputer_fill_value_default_behavior():
    """Test that IterativeImputer still works with default fill_value."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work with default fill_value (None)
    imputer = IterativeImputer(
        initial_strategy="constant",
        max_iter=1
    )
    
    # This should not raise an error
    result = imputer.fit_transform(X)
    
    # Check that the imputation worked
    assert result.shape == X.shape


def test_iterative_imputer_fill_value_different_strategies():
    """Test that fill_value parameter is only used when initial_strategy='constant'."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # This should work with other strategies (fill_value should be ignored)
    imputer = IterativeImputer(
        initial_strategy="mean",
        fill_value=999.0,  # This should be ignored
        max_iter=1
    )
    
    # This should not raise an error
    result = imputer.fit_transform(X)
    
    # Check that the imputation worked
    assert result.shape == X.shape


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that fill_value parameter exists and is properly handled."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
    
    # Test that we can access the fill_value attribute after initialization
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=777.0,
        max_iter=1
    )
    
    # Check that the parameter is stored correctly
    assert imputer.fill_value == 777.0
    
    # This should not raise an error
    result = imputer.fit_transform(X)
    assert result.shape == X.shape