"""
Regression tests for PR #59141: REF: Make concat not stateful.

This test ensures that the changes to the concat function maintain the correct
behavior, particularly around parameter validation and handling of edge cases.
"""

import pytest

import pandas as pd
from pandas import DataFrame, Series


def test_concat_join_parameter_validation():
    """Test that join parameter validation works correctly."""
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    
    # Valid join values should work
    result_outer = pd.concat([df1, df2], join="outer")
    result_inner = pd.concat([df1, df2], join="inner")
    
    # Invalid join value should raise ValueError with specific message
    with pytest.raises(ValueError, match="Only can inner.*outer.*union"):
        pd.concat([df1, df2], join="invalid")


def test_concat_sort_parameter_validation():
    """Test that sort parameter validation works correctly."""
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    
    # Valid sort values should work
    result_bool = pd.concat([df1, df2], sort=True)
    result_bool_false = pd.concat([df1, df2], sort=False)
    
    # Invalid sort values should raise ValueError with specific message
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        pd.concat([df1, df2], sort="invalid")
    
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        pd.concat([df1, df2], sort=1)


def test_concat_scalar_input_error():
    """Test that scalar inputs raise appropriate TypeError."""
    df = DataFrame({"A": [1, 2]})
    s = Series([1, 2])
    
    # Scalar inputs should raise TypeError
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        pd.concat(df)
    
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        pd.concat(s)


def test_concat_empty_list_error():
    """Test that empty list raises appropriate ValueError."""
    with pytest.raises(ValueError, match="No objects to concatenate"):
        pd.concat([])


def test_concat_basic_functionality_preserved():
    """Test that basic concat functionality still works correctly."""
    # Test DataFrame concatenation
    df1 = DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = DataFrame({"A": [5, 6], "B": [7, 8]})
    
    result = pd.concat([df1, df2])
    assert result.shape == (4, 2)
    
    # Test Series concatenation
    s1 = Series([1, 2])
    s2 = Series([3, 4])
    
    result = pd.concat([s1, s2])
    assert result.shape == (4,)