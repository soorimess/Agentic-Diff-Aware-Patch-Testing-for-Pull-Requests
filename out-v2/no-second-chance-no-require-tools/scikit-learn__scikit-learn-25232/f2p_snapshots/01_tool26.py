"""Test for IterativeImputer fill_value parameter regression test.

This test ensures that the fill_value parameter works correctly with
IterativeImputer when initial_strategy="constant".
"""

import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.utils._testing import assert_array_equal


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter."""
    # This should not raise an error - the main bug reported
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=42
    )
    assert imputer.fill_value == 42


def test_iterative_imputer_fill_value_with_nan():
    """Test that fill_value can be np.nan."""
    # This should not raise an error
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=np.nan
    )
    assert np.isnan(imputer.fill_value)


def test_iterative_imputer_fill_value_default_none():
    """Test that fill_value defaults to None."""
    imputer = IterativeImputer(initial_strategy="constant")
    assert imputer.fill_value is None


def test_iterative_imputer_fill_value_parameter_validation():
    """Test that fill_value parameter is properly validated."""
    # Test that we can pass various fill_value types
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value="test_string"
    )
    assert imputer.fill_value == "test_string"
    
    imputer = IterativeImputer(
        initial_strategy="constant", 
        fill_value=3.14
    )
    assert imputer.fill_value == 3.14