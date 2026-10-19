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


def test_pearsonr_axis_negative_values():
    """Test axis parameter with negative values."""
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[7, 8, 9], [10, 11, 12]])
    
    try:
        # Test axis=-1 (should work the same as axis=1)
        result = stats.pearsonr(x, y, axis=-1)
        assert result.statistic.shape == (2,)
        
        # Should be equivalent to axis=1
        result1 = stats.pearsonr(x, y, axis=1)
        np.testing.assert_array_equal(result.statistic, result1.statistic)
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise


def test_pearsonr_axis_broadcasting():
    """Test broadcasting behavior with axis parameter."""
    # Test the examples from the PR documentation
    try:
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((8, 15))
        y = rng.standard_normal((8, 15))
        
        # Test the shape examples from the docstring
        result1 = stats.pearsonr(x, y, axis=0)
        assert result1.statistic.shape == (15,)
        
        result2 = stats.pearsonr(x, y, axis=1)
        assert result2.statistic.shape == (8,)
        
        # Test pairwise comparisons
        result3 = stats.pearsonr(x[:, np.newaxis, :], y, axis=-1)
        assert result3.statistic.shape == (8, 8)
        
    except TypeError as e:
        # In the old version, this will raise TypeError about unexpected keyword argument
        if 'axis' in str(e) or 'unexpected keyword argument' in str(e):
            raise AssertionError("axis parameter not available in this version - this test should pass after the PR is applied")
        else:
            raise