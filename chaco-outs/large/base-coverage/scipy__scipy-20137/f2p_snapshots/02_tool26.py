"""
Regression tests for PR #20137: ENH: stats.pearsonr: add support for `axis` argument

This test ensures that the axis argument functionality works correctly
and that the behavior matches what was implemented in the pull request.
"""
import numpy as np
from scipy import stats


def test_pearsonr_axis_parameter_exists_and_works():
    """Test that axis parameter can be passed and basic functionality works."""
    # Simple 1D case - should work in both versions, but axis behavior differs
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    
    # Try to use the axis parameter - this should work in the new version
    try:
        result = stats.pearsonr(x, y, axis=0)
        # If we get here, the parameter exists and works
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        # Basic sanity check - should be a scalar
        assert np.isscalar(result.statistic) or result.statistic.shape == ()
        # Should be a reasonable correlation value
        assert -1.0 <= result.statistic <= 1.0
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise


def test_pearsonr_axis_2d_column_wise():
    """Test axis=0 (column-wise correlation) with 2D arrays."""
    # Create 2D arrays
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[7, 8, 9], [10, 11, 12]])
    
    try:
        # Test axis=0 (column-wise correlation) - should return shape (3,)
        result = stats.pearsonr(x, y, axis=0)
        assert result.statistic.shape == (3,)
        
        # Each correlation should be in [-1, 1]
        assert np.all(np.abs(result.statistic) <= 1.0)
        
        # Test that we get the right number of correlations (one per column)
        assert len(result.statistic) == 3
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise


def test_pearsonr_axis_2d_row_wise():
    """Test axis=1 (row-wise correlation) with 2D arrays."""
    # Create 2D arrays
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[7, 8, 9], [10, 11, 12]])
    
    try:
        # Test axis=1 (row-wise correlation) - should return shape (2,)
        result = stats.pearsonr(x, y, axis=1)
        assert result.statistic.shape == (2,)
        
        # Each correlation should be in [-1, 1]
        assert np.all(np.abs(result.statistic) <= 1.0)
        
        # Test that we get the right number of correlations (one per row)
        assert len(result.statistic) == 2
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise


def test_pearsonr_axis_none_behavior():
    """Test axis=None behavior (should ravel arrays)."""
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[7, 8, 9], [10, 11, 12]])
    
    try:
        # With axis=None, arrays should be raveled first
        result = stats.pearsonr(x, y, axis=None)
        assert result.statistic.shape == ()
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise


def test_pearsonr_axis_validation():
    """Test axis parameter validation."""
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    
    try:
        # Test non-integer axis should raise error
        stats.pearsonr(x, y, axis=0.5)
        # If it doesn't raise, that's unexpected
        assert False, "Should have raised ValueError for non-integer axis"
    except ValueError as e:
        assert 'axis' in str(e) or 'must be an integer' in str(e)
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise