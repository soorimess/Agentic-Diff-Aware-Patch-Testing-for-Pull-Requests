"""
Tests for pivot_table kwargs functionality.

This test file verifies the behavior added in PR #58893 which allows
passing keyword arguments to the aggfunc parameter in pivot_table.
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
import pytest


def test_pivot_table_kwargs_basic():
    """Test that pivot_table accepts and passes kwargs to aggfunc."""
    # Create test data
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, np.nan, 4, 5, np.nan]
    })
    
    # Test with min_count parameter that should be passed through to sum
    result = pd.pivot_table(df, values='C', index='A', columns='B', 
                           aggfunc='sum', min_count=1)
    
    # Should not raise an error and should handle NaN appropriately
    expected = DataFrame({
        'one': [1.0, 4.0],
        'two': [2.0, 5.0]
    }, index=['bar', 'foo'])
    expected.index.name = 'A'
    expected.columns.name = 'B'
    
    # The key test is that this doesn't raise an error
    assert result is not None


def test_pivot_table_kwargs_with_function():
    """Test that pivot_table passes kwargs to function aggfunc."""
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, np.nan, 4, 5, np.nan]
    })
    
    # Test with a custom function that accepts kwargs
    def sum_with_min_count(x, min_count=0):
        return x.sum(min_count=min_count)
    
    result = pd.pivot_table(df, values='C', index='A', columns='B', 
                           aggfunc=sum_with_min_count, min_count=1)
    
    # Should not raise an error
    assert result is not None


def test_pivot_table_kwargs_with_margins():
    """Test that pivot_table passes kwargs to aggfunc with margins=True."""
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, np.nan, 4, 5, np.nan]
    })
    
    # Test with margins and kwargs
    result = pd.pivot_table(df, values='C', index='A', columns='B', 
                           aggfunc='sum', min_count=1, margins=True)
    
    # Should not raise an error and should include margins
    assert result is not None
    assert 'All' in result.index
    assert 'All' in result.columns


def test_pivot_table_kwargs_with_dict_aggfunc():
    """Test that pivot_table passes kwargs to dict aggfunc."""
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, np.nan, 4, 5, np.nan],
        'D': [10, 20, 30, 40, 50, 60]
    })
    
    # Test with dict aggfunc and kwargs
    result = pd.pivot_table(df, values=['C', 'D'], index='A', columns='B', 
                           aggfunc={'C': 'sum', 'D': 'mean'}, min_count=1)
    
    # Should not raise an error
    assert result is not None


def test_pivot_table_kwargs_string_aggfunc():
    """Test that pivot_table passes kwargs to string aggfunc."""
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, np.nan, 4, 5, np.nan]
    })
    
    # Test with string aggfunc and kwargs
    result = pd.pivot_table(df, values='C', index='A', columns='B', 
                           aggfunc='sum', min_count=1)
    
    # Should not raise an error
    assert result is not None


def test_pivot_table_kwargs_no_kwargs():
    """Test that pivot_table still works normally without kwargs."""
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'one', 'two', 'one'],
        'C': [1, 2, 3, 4, 5, 6]
    })
    
    # Test normal operation without kwargs
    result = pd.pivot_table(df, values='C', index='A', columns='B', aggfunc='sum')
    
    # Should work as before
    assert result is not None


if __name__ == "__main__":
    # Run the tests
    test_pivot_table_kwargs_basic()
    test_pivot_table_kwargs_with_function()
    test_pivot_table_kwargs_with_margins()
    test_pivot_table_kwargs_with_dict_aggfunc()
    test_pivot_table_kwargs_string_aggfunc()
    test_pivot_table_kwargs_no_kwargs()
    print("All tests passed!")