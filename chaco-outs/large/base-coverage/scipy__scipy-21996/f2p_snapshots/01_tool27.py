import numpy as np
import pytest
from scipy import stats
from scipy.stats._stats_py import fisher_exact, SignificanceResult


def test_fisher_exact_2x2():
    """Test that 2x2 tables still work as before."""
    # Standard 2x2 table
    table = [[10, 5], [8, 12]]
    result = fisher_exact(table)
    
    # Check that we get expected results for 2x2 case
    assert isinstance(result, SignificanceResult)
    assert np.isfinite(result.statistic)
    assert 0 <= result.pvalue <= 1


def test_fisher_exact_rc_table_works_with_method():
    """Test that R x C tables work with method parameter."""
    # 3x3 table with MonteCarloMethod - should work after the change
    table = [[10, 5, 3], [8, 12, 7], [2, 4, 6]]
    rng = np.random.default_rng(4507195762371367)
    method = stats.MonteCarloMethod(rng=rng)
    
    # This should work with the new implementation
    result = fisher_exact(table, method=method)
    
    assert isinstance(result, SignificanceResult)
    assert np.isfinite(result.statistic)
    assert 0 <= result.pvalue <= 1


def test_fisher_exact_1x3_table():
    """Test 1x3 table behavior - should return (1.0, 1.0)."""
    table = [[10, 5, 3]]
    
    # Should return (1.0, 1.0) - only one table with fixed marginals
    result = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert isinstance(result, SignificanceResult)
    assert result.statistic == 1.0
    assert result.pvalue == 1.0


def test_fisher_exact_3x1_table():
    """Test 3x1 table behavior - should return (1.0, 1.0)."""
    table = [[10], [5], [3]]
    
    # Should return (1.0, 1.0) - only one table with fixed marginals
    result = fisher_exact(table, method=stats.MonteCarloMethod())
    
    assert isinstance(result, SignificanceResult)
    assert result.statistic == 1.0
    assert result.pvalue == 1.0


def test_fisher_exact_2x2_with_alternative():
    """Test that alternative parameter works for 2x2 tables."""
    table = [[10, 5], [8, 12]]
    
    # Test different alternative hypotheses
    result_two_sided = fisher_exact(table, alternative='two-sided')
    result_less = fisher_exact(table, alternative='less')
    result_greater = fisher_exact(table, alternative='greater')
    
    assert isinstance(result_two_sided, SignificanceResult)
    assert isinstance(result_less, SignificanceResult)
    assert isinstance(result_greater, SignificanceResult)


def test_fisher_exact_rc_with_invalid_alternative():
    """Test that alternative parameter raises error for R x C tables."""
    table = [[10, 5, 3], [8, 12, 7]]
    
    with pytest.raises(ValueError, match="`alternative` must be the default"):
        fisher_exact(table, alternative='two-sided', method=stats.MonteCarloMethod())


def test_fisher_exact_negative_values():
    """Test negative values raise error."""
    table = [[10, -5], [8, 12]]
    
    with pytest.raises(ValueError, match="All values in `table` must be nonnegative"):
        fisher_exact(table)


def test_fisher_exact_non_2d_table():
    """Test non-2D table raises error."""
    table = [[[10, 5], [8, 12]]]  # 3D array
    
    with pytest.raises(ValueError, match="The input `table` must have two dimensions"):
        fisher_exact(table)


def test_fisher_exact_2x2_with_invalid_alternative():
    """Test that invalid alternative raises error for 2x2 tables."""
    table = [[10, 5], [8, 12]]
    
    with pytest.raises(ValueError, match="`alternative` should be one of"):
        fisher_exact(table, alternative='invalid')