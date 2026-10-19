"""
Regression tests for PR #20137: ENH: stats.pearsonr: add support for `axis` argument

This test ensures that the axis argument functionality works correctly
and that the behavior matches what was implemented in the pull request.
"""
import numpy as np
from scipy import stats


def test_pearsonr_axis_parameter_basic():
    """Test that axis parameter can be passed and works correctly."""
    # Simple 1D case - should work in both versions, but axis behavior differs
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    
    # Try to use the axis parameter - this should work in the new version
    # but raise TypeError in the old version
    try:
        result = stats.pearsonr(x, y, axis=0)
        # If we get here, the parameter exists and works
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        # Basic sanity check
        assert np.isscalar(result.statistic) or result.statistic.shape == ()
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            # This is expected in the old version - we're testing that it's missing
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            # Some other TypeError, re-raise it
            raise


def test_pearsonr_axis_2d_basic():
    """Test basic 2D axis functionality."""
    # Create 2D arrays
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[7, 8, 9], [10, 11, 12]])
    
    try:
        # Test axis=0 (column-wise correlation) - should return shape (3,)
        result = stats.pearsonr(x, y, axis=0)
        assert result.statistic.shape == (3,)
        
        # Test axis=1 (row-wise correlation) - should return shape (2,)
        result = stats.pearsonr(x, y, axis=1)
        assert result.statistic.shape == (2,)
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise