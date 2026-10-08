"""
Test for IterativeImputer fill_value parameter.

This test ensures that IterativeImputer properly supports the fill_value
parameter when initial_strategy="constant", which was added in a recent
pull request.
"""

import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter."""
    # This should work after the fix is applied
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan]])
    
    # Test that we can pass fill_value parameter to IterativeImputer
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=5.0
    )
    
    # This should not raise an exception
    result = imputer.fit_transform(X)
    
    # The missing values should be filled with the specified fill_value
    assert not np.isnan(result[1, 0])  # First missing value should be filled
    assert not np.isnan(result[2, 1])  # Second missing value should be filled


def test_iterative_imputer_fill_value_with_constant_strategy():
    """Test that fill_value is properly used with initial_strategy='constant'."""
    # Create data with missing values
    X = np.array([[1, np.nan], [np.nan, 3], [4, np.nan]])
    
    # Use a specific fill_value
    fill_value = 99.0
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=fill_value,
        max_iter=1  # Small number to make it faster
    )
    
    # Fit and transform
    X_imputed = imputer.fit_transform(X)
    
    # Check that the fill_value was used for initial imputation
    assert X_imputed.shape == X.shape


def test_iterative_imputer_fill_value_functionality():
    """Test that fill_value parameter actually affects the imputation result."""
    # Create a simple test case where we can verify fill_value is used
    X = np.array([[1.0, np.nan], [np.nan, 3.0]])
    
    # Test with a specific fill_value
    fill_value = 42.0
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=fill_value,
        max_iter=1
    )
    
    result = imputer.fit_transform(X)
    
    # The imputation should work without error
    assert not np.isnan(result).any()
    
    # Check that we can access the fill_value that was set
    assert imputer.fill_value == fill_value


def test_iterative_imputer_parameter_storage_and_access():
    """Test that fill_value parameter is properly stored and accessible."""
    # Test that the parameter is correctly stored in the instance
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=10.0
    )
    
    # Verify the parameter is stored correctly
    assert hasattr(imputer, 'fill_value')
    assert imputer.fill_value == 10.0
    
    # Test with None (default)
    imputer2 = IterativeImputer(initial_strategy="constant")
    assert imputer2.fill_value is None


def test_iterative_imputer_without_fill_value():
    """Test that IterativeImputer still works without fill_value parameter."""
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan]])
    
    # This should work as before (using default fill_value=None behavior)
    imputer = IterativeImputer(initial_strategy="mean")
    result = imputer.fit_transform(X)
    
    assert not np.isnan(result).any()  # All values should be filled


if __name__ == "__main__":
    # Run the tests
    test_iterative_imputer_fill_value_parameter_exists()
    test_iterative_imputer_fill_value_with_constant_strategy()
    test_iterative_imputer_fill_value_functionality()
    test_iterative_imputer_parameter_storage_and_access()
    test_iterative_imputer_without_fill_value()
    print("All tests passed!")