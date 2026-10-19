"""
Test for pearsonr axis argument functionality.

This test ensures that the axis argument in pearsonr works correctly
for multi-dimensional arrays, as added in PR #20137.
"""
import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pytest
from scipy import stats


class TestPearsonRAxis:
    def test_pearsonr_axis_basic(self):
        """Test basic functionality of axis argument with 2D arrays."""
        # Create test data
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((8, 15))
        y = rng.standard_normal((8, 15))
        
        # Test axis=0 (default behavior)
        result_axis0 = stats.pearsonr(x, y, axis=0)
        assert result_axis0.statistic.shape == (15,)
        
        # Test axis=1
        result_axis1 = stats.pearsonr(x, y, axis=1)
        assert result_axis1.statistic.shape == (8,)
        
        # Test that the results have different shapes (they should be different)
        assert result_axis0.statistic.shape != result_axis1.statistic.shape
    
    def test_pearsonr_axis_none(self):
        """Test axis=None behavior."""
        # Create test data
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((8, 15))
        y = rng.standard_normal((8, 15))
        
        # Test axis=None (should ravel arrays)
        result_none = stats.pearsonr(x, y, axis=None)
        assert result_none.statistic.shape == ()
        
        # Should be equivalent to flattening the arrays
        result_flat = stats.pearsonr(x.ravel(), y.ravel())
        assert_allclose(result_none.statistic, result_flat.statistic)
    
    def test_pearsonr_axis_multidim(self):
        """Test axis argument with 3D arrays."""
        # Create 3D test data
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((3, 4, 5))
        y = rng.standard_normal((3, 4, 5))
        
        # Test axis=0
        result_axis0 = stats.pearsonr(x, y, axis=0)
        assert result_axis0.statistic.shape == (4, 5)
        
        # Test axis=1
        result_axis1 = stats.pearsonr(x, y, axis=1)
        assert result_axis1.statistic.shape == (3, 5)
        
        # Test axis=2
        result_axis2 = stats.pearsonr(x, y, axis=2)
        assert result_axis2.statistic.shape == (3, 4)
    
    def test_pearsonr_axis_1d(self):
        """Test that 1D arrays still work with axis parameter."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])
        
        result = stats.pearsonr(x, y, axis=0)
        assert result.statistic.shape == ()
        
        # Should match regular 1D behavior
        result_regular = stats.pearsonr(x, y)
        assert_allclose(result.statistic, result_regular.statistic)
    
    def test_pearsonr_axis_with_alternative(self):
        """Test axis argument with alternative parameter."""
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((8, 15))
        y = rng.standard_normal((8, 15))
        
        # Test with alternative='greater'
        result = stats.pearsonr(x, y, axis=0, alternative='greater')
        assert result.statistic.shape == (15,)
        
        # Test with alternative='less'
        result = stats.pearsonr(x, y, axis=0, alternative='less')
        assert result.statistic.shape == (15,)
    
    def test_pearsonr_axis_with_method(self):
        """Test axis argument with method parameter."""
        rng = np.random.default_rng(2348246935601934321)
        x = rng.standard_normal((8, 15))
        y = rng.standard_normal((8, 15))
        
        # Test with permutation method
        method = stats.PermutationMethod(n_resamples=100)
        result = stats.pearsonr(x, y, axis=0, method=method)
        assert result.statistic.shape == (15,)
        
        # Test with MonteCarlo method
        method = stats.MonteCarloMethod(n_resamples=100)
        result = stats.pearsonr(x, y, axis=0, method=method)
        assert result.statistic.shape == (15,)
    
    def test_pearsonr_axis_errors(self):
        """Test error conditions for axis argument."""
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        
        # Test invalid axis type
        with pytest.raises(ValueError, match='`axis` must be an integer'):
            stats.pearsonr(x, y, axis=0.5)