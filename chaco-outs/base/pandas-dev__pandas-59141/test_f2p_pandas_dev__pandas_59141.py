"""
Regression tests for PR #59141: REF: Make concat not stateful.

This test ensures that the validation of join and sort parameters works correctly
and that concat behaves as expected after the refactoring.
"""
import pytest

import pandas as pd
from pandas import DataFrame, Series


def test_concat_join_parameter_validation():
    """Test that join parameter only accepts 'outer' or 'inner'."""
    s1 = Series([1, 2])
    s2 = Series([3, 4])
    
    # Valid join values should work
    result_outer = pd.concat([s1, s2], join="outer")
    result_inner = pd.concat([s1, s2], join="inner")
    
    # Invalid join values should raise ValueError
    with pytest.raises(ValueError, match="Only can inner.*outer.*join"):
        pd.concat([s1, s2], join="invalid")


def test_concat_sort_parameter_validation():
    """Test that sort parameter only accepts boolean values."""
    s1 = Series([1, 2])
    s2 = Series([3, 4])
    
    # Valid boolean sort values should work
    result_false = pd.concat([s1, s2], sort=False)
    result_true = pd.concat([s1, s2], sort=True)
    
    # Invalid sort values should raise ValueError
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        pd.concat([s1, s2], sort="invalid")
    
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        pd.concat([s1, s2], sort=1)


def test_concat_invalid_input_type():
    """Test that concat raises TypeError for invalid input types."""
    # Test with a single Series (should raise TypeError)
    s1 = Series([1, 2])
    
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        pd.concat(s1)
    
    # Test with a single DataFrame (should raise TypeError)  
    df1 = DataFrame({"A": [1, 2]})
    
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        pd.concat(df1)


def test_concat_with_empty_list():
    """Test that concat with empty list raises appropriate error."""
    with pytest.raises(ValueError, match="No objects to concatenate"):
        pd.concat([])


def test_concat_basic_functionality():
    """Test basic concat functionality works correctly."""
    # Test Series concatenation
    s1 = Series([1, 2])
    s2 = Series([3, 4])
    result = pd.concat([s1, s2])
    expected = Series([1, 2, 3, 4], index=[0, 1, 0, 1])
    pd.testing.assert_series_equal(result, expected)
    
    # Test DataFrame concatenation
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    result = pd.concat([df1, df2])
    expected = DataFrame({"A": [1, 2, 3, 4]}, index=[0, 1, 0, 1])
    pd.testing.assert_frame_equal(result, expected)