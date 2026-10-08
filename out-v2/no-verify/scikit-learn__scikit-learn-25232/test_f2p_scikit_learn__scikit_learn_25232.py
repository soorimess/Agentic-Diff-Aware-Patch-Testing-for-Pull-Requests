"""
Test for IterativeImputer fill_value parameter.

This test verifies that IterativeImputer properly supports the fill_value
parameter when initial_strategy="constant", which was added in version 1.3.
"""

import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter without error."""
    # This should not raise TypeError: __init__() got an unexpected keyword argument 'fill_value'
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=42.0
    )
    
    # Just verify we can create the object - the main point is no TypeError
    assert imputer is not None


def test_iterative_imputer_fill_value_parameter_with_none():
    """Test that IterativeImputer accepts fill_value=None."""
    # This should not raise TypeError even with fill_value=None
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=None
    )
    
    # Just verify we can create the object
    assert imputer is not None


def test_iterative_imputer_fill_value_parameter_with_string():
    """Test that IterativeImputer accepts string fill_value."""
    # This should not raise TypeError with string fill_value
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value="missing_value"
    )
    
    # Just verify we can create the object
    assert imputer is not None