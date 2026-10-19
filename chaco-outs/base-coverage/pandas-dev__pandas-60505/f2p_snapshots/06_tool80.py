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


def test_groupby_apply_empty_dataframe_group_keys_behavior_distinction():
    """
    Test that group_keys=False and group_keys=True produce different index types
    for empty DataFrames, which is the core fix being tested.
    
    This test specifically catches the mutation that would incorrectly apply the fix
    when group_keys=True instead of when group_keys=False.
    """
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Create empty DataFrame
        df = DataFrame({'A': [], 'B': [], 'C': []})
        
        # Test group_keys=False case - should return RangeIndex (the fix)
        g_false = df.groupby('A', group_keys=False)
        result_false = g_false.apply(lambda x: x)
        
        # Test group_keys=True case - should NOT return RangeIndex (preserve existing behavior)
        g_true = df.groupby('A', group_keys=True)
        result_true = g_true.apply(lambda x: x)
        
        # The fix ensures these two cases return different index types:
        # group_keys=False: RangeIndex (this is what we're fixing)
        # group_keys=True: Index with group keys (this should remain unchanged)
        
        # This assertion specifically catches the mutation:
        # If the mutation was applied, group_keys=True would incorrectly return RangeIndex
        assert isinstance(result_false.index, pd.RangeIndex), "group_keys=False should return RangeIndex"
        assert not isinstance(result_true.index, pd.RangeIndex), "group_keys=True should NOT return RangeIndex"
        assert result_true.index.name == 'A', "group_keys=True should have group name in index"
        
        # Verify they are indeed different (both should be empty but different types)
        assert len(result_false.index) == 0
        assert len(result_true.index) == 0