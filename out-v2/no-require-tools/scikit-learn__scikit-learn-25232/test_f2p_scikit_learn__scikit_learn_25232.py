"""
Regression test for IterativeImputer fill_value parameter.

This test ensures that IterativeImputer properly supports the fill_value
parameter when initial_strategy="constant", which was missing in the original
implementation.
"""
import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter."""
    # This should not raise an error - the main assertion
    imputer = IterativeImputer(initial_strategy="constant", fill_value=5.0)
    assert hasattr(imputer, 'fill_value')
    assert imputer.fill_value == 5.0


def test_iterative_imputer_fill_value_stored_correctly():
    """Test that fill_value is properly stored as an instance attribute."""
    # Test various fill_value types
    imputer = IterativeImputer(initial_strategy="constant", fill_value=42.0)
    assert imputer.fill_value == 42.0
    
    imputer = IterativeImputer(initial_strategy="constant", fill_value=-1.5)
    assert imputer.fill_value == -1.5
    
    imputer = IterativeImputer(initial_strategy="constant", fill_value=None)
    assert imputer.fill_value is None


def test_iterative_imputer_fill_value_default_none():
    """Test that default fill_value is None."""
    imputer = IterativeImputer(initial_strategy="constant")
    assert imputer.fill_value is None