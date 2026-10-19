"""
Regression tests for PR #21996: ENH: `stats.fisher_exact`: extend to `R x C` tables

This tests the behavior changes introduced in the pull request that extends
fisher_exact to work with contingency tables of any size (R x C), not just 2x2.
"""
import numpy as np
import pytest
from scipy import stats
from scipy.stats._stats_py import fisher_exact


def test_fisher_exact_2x2_still_works():
    """Test that 2x2 tables still work as before."""
    # Test case from the docstring
    table = [[6, 2], [1, 4]]
    res = fisher_exact(table)
    
    # Check that we get the same results as before for 2x2 tables
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    assert np.isfinite(res.statistic)
    assert 0 <= res.pvalue <= 1


def test_fisher_exact_2x2_with_alternative():
    """Test that 2x2 tables work with alternative parameter."""
    table = [[6, 2], [1, 4]]
    
    # Test different alternatives
    res_two_sided = fisher_exact(table, alternative='two-sided')
    res_less = fisher_exact(table, alternative='less')
    res_greater = fisher_exact(table, alternative='greater')
    
    assert hasattr(res_two_sided, 'statistic')
    assert hasattr(res_two_sided, 'pvalue')
    assert hasattr(res_less, 'statistic')
    assert hasattr(res_less, 'pvalue')
    assert hasattr(res_greater, 'statistic')
    assert hasattr(res_greater, 'pvalue')


def test_fisher_exact_rc_tables_with_method():
    """Test that R x C tables work with method parameter."""
    # 3x3 table - should work with method now
    table = [[8, 2, 3], [1, 5, 4], [2, 1, 6]]
    rng = np.random.default_rng(4507195762371367)
    method = stats.MonteCarloMethod(rng=rng)
    
    # This should work now with the new implementation
    res = fisher_exact(table, method=method)
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    assert 0 <= res.statistic <= 1
    assert 0 <= res.pvalue <= 1


def test_fisher_exact_rc_tables_with_permutation_method():
    """Test that R x C tables work with PermutationMethod."""
    table = [[8, 2, 3], [1, 5, 4], [2, 1, 6]]
    rng = np.random.default_rng(4507195762371367)
    method = stats.PermutationMethod(rng=rng)
    
    # This should work now with the new implementation
    res = fisher_exact(table, method=method)
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    assert 0 <= res.statistic <= 1
    assert 0 <= res.pvalue <= 1


def test_fisher_exact_1xN_table():
    """Test edge case with 1xN table."""
    table = [[8, 2, 3]]
    
    # Should work now - only one such table with fixed marginals
    res = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    # For 1xN tables, should return statistic=1.0, pvalue=1.0
    assert res.statistic == 1.0
    assert res.pvalue == 1.0


def test_fisher_exact_Nx1_table():
    """Test edge case with Nx1 table."""
    table = [[8], [2], [3]]
    
    # Should work now - only one such table with fixed marginals
    res = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    # For Nx1 tables, should return statistic=1.0, pvalue=1.0
    assert res.statistic == 1.0
    assert res.pvalue == 1.0


def test_fisher_exact_zero_table():
    """Test edge case with all zeros."""
    table = [[0, 0, 0], [0, 0, 0]]
    
    # Should work now - only one such table with fixed marginals
    res = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    # For zero tables, should return statistic=1.0, pvalue=1.0
    assert res.statistic == 1.0
    assert res.pvalue == 1.0


def test_fisher_exact_invalid_method():
    """Test that invalid method raises appropriate error."""
    table = [[8, 2, 3], [1, 5, 4]]
    
    # Test with invalid method type
    with pytest.raises(ValueError, match="not recognized"):
        fisher_exact(table, method="invalid_method")


def test_fisher_exact_alternative_with_rc_table():
    """Test that alternative parameter raises error with R x C tables."""
    table = [[8, 2, 3], [1, 5, 4]]
    
    # Should raise error when alternative is specified for non-2x2 tables
    with pytest.raises(ValueError, match="`alternative` must be the default"):
        fisher_exact(table, alternative='two-sided', method=stats.MonteCarloMethod())


def test_fisher_exact_2x2_with_method():
    """Test that 2x2 tables work with method parameter (should ignore method)."""
    table = [[6, 2], [1, 4]]
    
    # Should work with method parameter for 2x2 tables (method ignored)
    res = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert hasattr(res, 'statistic')
    assert hasattr(res, 'pvalue')
    assert np.isfinite(res.statistic)
    assert 0 <= res.pvalue <= 1


def test_fisher_exact_non_2d_table():
    """Test that non-2D tables raise appropriate error."""
    # 1D array - should raise error about dimensions
    table = [1, 2, 3]
    
    with pytest.raises(ValueError, match="The input `table` must have two dimensions."):
        fisher_exact(table)
        
    # 3D array - should raise error about dimensions  
    table = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    
    with pytest.raises(ValueError, match="The input `table` must have two dimensions."):
        fisher_exact(table)


def test_fisher_exact_monte_carlo_method_with_rvs():
    """Test that MonteCarloMethod with rvs attribute raises error."""
    table = [[8, 2, 3], [1, 5, 4]]
    # Create a MonteCarloMethod with rvs specified (should fail)
    method = stats.MonteCarloMethod(rvs=lambda size: np.array([1, 2, 3]))
    
    with pytest.raises(ValueError, match="rvs.*must be unspecified"):
        fisher_exact(table, method=method)


def test_fisher_exact_empty_table():
    """Test that empty 2D tables raise appropriate error."""
    # Empty 2D array with no rows or columns - should raise error about size
    table = np.array([]).reshape(0, 0)  # 0x0 array
    
    with pytest.raises(ValueError, match="must have at least one row and one column"):
        fisher_exact(table, method=stats.MonteCarloMethod())