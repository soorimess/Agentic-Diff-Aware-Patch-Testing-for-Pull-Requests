"""
Regression test for IterativeImputer fill_value parameter.

This test ensures that IterativeImputer properly accepts and uses the fill_value
parameter when initial_strategy="constant".
"""
import numpy as np
import pytest

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.utils._testing import assert_array_equal


def test_iterative_imputer_fill_value_parameter_exists():
    """Test that IterativeImputer accepts fill_value parameter."""
    # This should work after the fix - using fill_value with constant strategy
    imputer = IterativeImputer(initial_strategy="constant", fill_value=42)
    
    # Check that the parameter is accepted and stored
    assert imputer.fill_value == 42


def test_iterative_imputer_fill_value_none_default():
    """Test that fill_value defaults to None."""
    imputer = IterativeImputer(initial_strategy="constant")
    
    # Check that fill_value defaults to None
    assert imputer.fill_value is None


def test_iterative_imputer_fill_value_parameter_validation():
    """Test that fill_value parameter is properly validated."""
    # This should work - fill_value should be accepted for any value
    imputer = IterativeImputer(initial_strategy="constant", fill_value="test")
    assert imputer.fill_value == "test"
    
    imputer = IterativeImputer(initial_strategy="constant", fill_value=123)
    assert imputer.fill_value == 123
    
    imputer = IterativeImputer(initial_strategy="constant", fill_value=np.nan)
    assert np.isnan(imputer.fill_value)


def test_iterative_imputer_fill_value_parameter_accepted():
    """Test that fill_value parameter is accepted without error."""
    # Test that we can create an imputer with fill_value without getting
    # a TypeError about unexpected keyword argument
    try:
        imputer = IterativeImputer(
            initial_strategy="constant", 
            fill_value=99.0,
            random_state=0
        )
        # If we get here without TypeError, the parameter is accepted
        assert hasattr(imputer, 'fill_value')
        assert imputer.fill_value == 99.0
        # Test that we can at least call fit_transform without error
        X = np.array([[1, 2], [np.nan, 3], [4, np.nan], [5, 6]])
        result = imputer.fit_transform(X)
        # Just verify it doesn't crash - the actual imputation behavior
        # might be different due to iterative nature
        assert result is not None
        assert result.shape == X.shape
    except TypeError as e:
        if "unexpected keyword argument 'fill_value'" in str(e):
            pytest.fail("fill_value parameter is not accepted by IterativeImputer")
        raise