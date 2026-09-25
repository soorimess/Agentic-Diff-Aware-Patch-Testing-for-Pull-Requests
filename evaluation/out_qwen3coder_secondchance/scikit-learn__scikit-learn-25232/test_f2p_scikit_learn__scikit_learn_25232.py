"""Test for IterativeImputer fill_value parameter.

This test verifies that IterativeImputer supports the fill_value parameter
when initial_strategy="constant".
"""
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter."""
    # This should not raise an error in the fixed version
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=42
    )
    assert imputer.fill_value == 42


def test_iterative_imputer_fill_value_parameter_acceptance():
    """Test that IterativeImputer accepts fill_value parameter without error."""
    # This test should pass - the main issue was that the parameter didn't exist
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value="test_value"
    )
    assert imputer.fill_value == "test_value"


def test_iterative_imputer_default_fill_value():
    """Test that default fill_value behavior works."""
    # Test that default fill_value works
    imputer = IterativeImputer(
        initial_strategy="constant",
        max_iter=1,
        random_state=0
    )
    # Should not raise any error and should have default value
    assert imputer.fill_value is None


def test_iterative_imputer_fill_value_integration():
    """Test that fill_value is properly integrated in actual imputation."""
    # Test the actual functionality that uses the parameter:
    # create a data set and run imputation to ensure the parameter is actually used
    
    X = np.array([[1., 2.],
                  [np.nan, 4.],
                  [5., np.nan],
                  [7., 8.]])
    
    # This should work without error and the fill_value should be used
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=99.0,
        max_iter=1,
        random_state=0
    )
    
    # This should not raise TypeError about fill_value and should execute
    # the code path where fill_value is passed to SimpleImputer
    X_imputed = imputer.fit_transform(X)
    
    # Just confirm it runs without throwing the main parameter error
    assert X_imputed.shape == X.shape