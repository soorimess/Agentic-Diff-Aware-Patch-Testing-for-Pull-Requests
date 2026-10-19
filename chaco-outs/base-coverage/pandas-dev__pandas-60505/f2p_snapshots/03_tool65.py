"""
Regression test for issue #60471: BUG: DataFrameGroupBy.apply ignores group_keys 
setting when empty

Tests that DataFrameGroupBy.apply respects the group_keys parameter when dealing 
with empty dataframes.
"""
import pandas as pd
from pandas import DataFrame
import warnings


def test_groupby_apply_empty_dataframe_group_keys_false():
    """
    Test that DataFrameGroupBy.apply with group_keys=False on empty DataFrame
    returns a result with RangeIndex (not index with group keys).
    
    This test verifies the fix for issue #60471 where group_keys=False was 
    incorrectly returning an index with group keys instead of a RangeIndex.
    """
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Create empty DataFrame
        df = DataFrame({'A': [], 'B': [], 'C': []})
        g2 = df.groupby('A', group_keys=False)
        
        # Apply function - this should return RangeIndex after fix
        result = g2.apply(lambda x: x)
        
        # The fix ensures that when group_keys=False, we get RangeIndex instead of 
        # Index with group keys. This assertion will pass after the fix is applied.
        # Before fix: result.index is Index([], dtype='float64', name='A') 
        # After fix: result.index is RangeIndex(start=0, stop=0, step=1)
        assert isinstance(result.index, pd.RangeIndex), f"Expected RangeIndex, got {type(result.index)}"
        assert len(result.index) == 0
        assert result.index.start == 0
        assert result.index.stop == 0
        assert result.index.step == 1


def test_groupby_apply_empty_dataframe_group_keys_true():
    """
    Test that DataFrameGroupBy.apply with group_keys=True on empty DataFrame
    returns a result with index containing group keys.
    
    This ensures that the behavior for group_keys=True is preserved.
    """
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Create empty DataFrame
        df = DataFrame({'A': [], 'B': [], 'C': []})
        g3 = df.groupby('A', group_keys=True)
        
        # Apply function - this should return index with group keys
        result = g3.apply(lambda x: x)
        
        # With group_keys=True, result should have index with group keys
        # This should be the same as the current (buggy) behavior for empty DataFrames
        assert result.index.name == 'A'
        assert len(result.index) == 0
        # When group_keys=True, we expect the index to contain group keys
        # This is the expected behavior (not the bug) - it's the same as current behavior
        assert not isinstance(result.index, pd.RangeIndex)


def test_groupby_apply_empty_series_group_keys_false():
    """
    Test that SeriesGroupBy.apply with group_keys=False on empty Series
    returns a result with RangeIndex.
    """
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Create empty Series
        s = pd.Series([], name='B', dtype='int64')
        g2 = s.groupby(s.index, group_keys=False)
        
        # Apply function - this should return RangeIndex after fix
        result = g2.apply(lambda x: x)
        
        # The fix ensures that when group_keys=False, we get RangeIndex instead of 
        # Index with group keys
        assert isinstance(result.index, pd.RangeIndex), f"Expected RangeIndex, got {type(result.index)}"
        assert len(result.index) == 0
        assert result.index.start == 0
        assert result.index.stop == 0
        assert result.index.step == 1


def test_behavior_difference_between_group_keys():
    """
    Test that demonstrates the expected behavior difference between 
    group_keys=False and group_keys=True for empty DataFrames.
    
    This test ensures that the fix properly distinguishes between the two cases.
    """
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Create empty DataFrame
        df = DataFrame({'A': [], 'B': [], 'C': []})
        
        # Test group_keys=False case
        g_false = df.groupby('A', group_keys=False)
        result_false = g_false.apply(lambda x: x)
        
        # Test group_keys=True case
        g_true = df.groupby('A', group_keys=True)
        result_true = g_true.apply(lambda x: x)
        
        # Verify they have different index types (the fix should make them different)
        # Before fix: both return Index([], dtype='float64', name='A')
        # After fix: group_keys=False returns RangeIndex, group_keys=True returns Index with group keys
        
        # The key assertion is that they should be different
        assert isinstance(result_false.index, pd.RangeIndex)
        assert not isinstance(result_true.index, pd.RangeIndex)
        assert result_true.index.name == 'A'