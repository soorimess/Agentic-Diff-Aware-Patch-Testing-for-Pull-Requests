"""
Regression test for issue #60471: BUG: DataFrameGroupBy.apply ignores group_keys setting when empty
"""
import pandas as pd
import pytest
from pandas import DataFrame
import warnings


def test_groupby_apply_empty_dataframe_group_keys_false():
    """
    Test that DataFrameGroupBy.apply with group_keys=False on empty DataFrame
    returns a RangeIndex instead of an Index with group keys.
    """
    # Create empty DataFrame
    df = DataFrame({'A': [], 'B': [], 'C': []})
    g2 = df.groupby('A', group_keys=False)
    
    # Suppress deprecation warning to focus on the actual behavior
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        result = g2.apply(lambda x: x / x.sum())
    
    # With group_keys=False, the result should have a RangeIndex(0, 0, 1)
    # not an Index with the group keys (this is the bug being fixed)
    assert isinstance(result.index, pd.RangeIndex)
    assert len(result.index) == 0
    assert result.index.start == 0
    assert result.index.stop == 0
    assert result.index.step == 1


def test_groupby_apply_empty_dataframe_group_keys_true():
    """
    Test that DataFrameGroupBy.apply with group_keys=True on empty DataFrame
    returns an Index with group keys.
    """
    # Create empty DataFrame
    df = DataFrame({'A': [], 'B': [], 'C': []})
    g3 = df.groupby('A', group_keys=True)
    
    # Suppress deprecation warning to focus on the actual behavior
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        result = g3.apply(lambda x: x / x.sum())
    
    # With group_keys=True, the result should have an Index with group keys
    assert isinstance(result.index, pd.Index)
    assert not isinstance(result.index, pd.RangeIndex)
    assert len(result.index) == 0
    assert result.index.name == 'A'