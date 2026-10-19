import numpy as np
import pytest
from scipy import stats
from scipy.stats._stats_py import fisher_exact, SignificanceResult


class TestFisherExactRxC:
    """Test cases for fisher_exact with R x C tables."""
    
    def test_2x2_table_still_works(self):
        """Test that 2x2 tables still work as before."""
        # Test case from the existing documentation
        table = [[8, 2], [1, 5]]
        result = fisher_exact(table)
        
        assert isinstance(result, SignificanceResult)
        assert np.isclose(result.statistic, 20.0)
        assert np.isclose(result.pvalue, 0.034965034965034975)
    
    def test_2x2_table_with_alternative(self):
        """Test that 2x2 tables still support alternative parameter."""
        table = [[8, 2], [1, 5]]
        
        # Test two-sided
        result = fisher_exact(table, alternative='two-sided')
        assert isinstance(result, SignificanceResult)
        assert np.isclose(result.pvalue, 0.034965034965034975)
        
        # Test less
        result = fisher_exact(table, alternative='less')
        assert isinstance(result, SignificanceResult)
        
        # Test greater
        result = fisher_exact(table, alternative='greater')
        assert isinstance(result, SignificanceResult)
    
    def test_3x3_table_works_with_method(self):
        """Test that 3x3 tables work with method parameter."""
        table = [[8, 2, 3], [1, 5, 4], [2, 1, 3]]
        rng = np.random.default_rng(4507195762371367)
        method = stats.MonteCarloMethod(rng=rng)
        
        result = fisher_exact(table, method=method)
        
        assert isinstance(result, SignificanceResult)
        assert isinstance(result.statistic, np.float64)
        assert isinstance(result.pvalue, np.float64)
        assert 0 <= result.pvalue <= 1
    
    def test_3x3_table_with_permutation_method(self):
        """Test that 3x3 tables work with PermutationMethod."""
        table = [[8, 2, 3], [1, 5, 4], [2, 1, 3]]
        rng = np.random.default_rng(4507195762371367)
        method = stats.PermutationMethod(rng=rng)
        
        result = fisher_exact(table, method=method)
        
        assert isinstance(result, SignificanceResult)
        assert isinstance(result.statistic, np.float64)
        assert isinstance(result.pvalue, np.float64)
        assert 0 <= result.pvalue <= 1
    
    def test_2x3_table_with_method(self):
        """Test that 2x3 tables work with method parameter."""
        table = [[8, 2, 3], [1, 5, 4]]
        rng = np.random.default_rng(4507195762371367)
        method = stats.MonteCarloMethod(rng=rng)
        
        result = fisher_exact(table, method=method)
        
        assert isinstance(result, SignificanceResult)
        assert isinstance(result.statistic, np.float64)
        assert isinstance(result.pvalue, np.float64)
        assert 0 <= result.pvalue <= 1
    
    def test_invalid_method_type(self):
        """Test that invalid method types raise ValueError."""
        table = [[8, 2, 3], [1, 5, 4]]
        rng = np.random.default_rng(4507195762371367)
        
        # Test with invalid method type
        with pytest.raises(ValueError, match="`method=.*` not recognized"):
            fisher_exact(table, method="invalid_method")
    
    def test_alternative_with_non_2x2_table(self):
        """Test that alternative parameter raises error with non-2x2 tables."""
        table = [[8, 2, 3], [1, 5, 4]]
        rng = np.random.default_rng(4507195762371367)
        method = stats.MonteCarloMethod(rng=rng)
        
        with pytest.raises(ValueError, match="`alternative` must be the default \\(None\\)"):
            fisher_exact(table, alternative='two-sided', method=method)
    
    def test_table_with_negative_values(self):
        """Test that tables with negative values raise ValueError."""
        table = [[8, -2], [1, 5]]
        
        with pytest.raises(ValueError, match="All values in `table` must be nonnegative."):
            fisher_exact(table)
    
    def test_table_with_zero_rows_or_cols(self):
        """Test that tables with zero rows or columns work correctly."""
        # Test with zero row
        table = [[0, 0, 0], [1, 5, 4]]
        rng = np.random.default_rng(4507195762371367)
        method = stats.MonteCarloMethod(rng=rng)
        
        result = fisher_exact(table, method=method)
        assert isinstance(result, SignificanceResult)
        # For tables with zero rows/columns, should return 1.0 for both statistic and pvalue
        assert result.statistic == 1.0
        assert result.pvalue == 1.0
    
    def test_empty_table(self):
        """Test that empty tables raise ValueError with new message."""
        table = []
        
        # After the change, this should raise the new error message
        with pytest.raises(ValueError, match="The input `table` must have two dimensions."):
            fisher_exact(table)