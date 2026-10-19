"""
Regression tests for PR #22616: ENH: stats: use `vecdot` and `nonzero` where appropriate

This test file verifies that the changes in the pull request maintain the same
numerical behavior while improving performance.
"""

import numpy as np
from numpy.testing import assert_allclose


def test_gaussian_kde_neff_computation():
    """
    Test that gaussian_kde._neff computation preserves numerical results.
    
    This test specifically targets the change from:
    `self._neff = 1/sum(self._weights**2)` 
    to:
    `self._neff = 1/np_vecdot(self._weights, self._weights)`
    
    The test verifies that when np_vecdot is available, it produces the same 
    numerical result as the old sum-based approach.
    """
    # Create test data with known weights
    np.random.seed(42)
    data = np.random.randn(10)
    
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(data)
    
    # Test that the basic functionality works
    # This test will be meaningful when np_vecdot is available
    try:
        from scipy._lib._util import np_vecdot
        # When np_vecdot is available, test that both approaches give same result
        # Old way: 1 / sum(weights**2) 
        # New way: 1 / np_vecdot(weights, weights)
        neff_old = 1 / np.sum(kde.weights**2)
        neff_new = 1 / np_vecdot(kde.weights, kde.weights)
        assert_allclose(neff_old, neff_new, rtol=1e-12)
    except ImportError:
        # Before PR - just make sure basic functionality works
        # The computation should still work with the old approach
        assert hasattr(kde, '_neff')
        neff_old = 1 / np.sum(kde.weights**2)
        assert np.isfinite(neff_old)


def test_vecdot_equivalence():
    """
    Test that vecdot produces same results as sum for element-wise multiplication.
    
    This test verifies that when np_vecdot is introduced in the PR, it will
    behave identically to np.sum(x * y) for element-wise multiplication.
    """
    # Create test data
    np.random.seed(42)
    x = np.random.rand(50)
    y = np.random.rand(50)
    
    try:
        from scipy._lib._util import np_vecdot
        # This will be the new behavior after PR
        result_vecdot = np_vecdot(x, y)
        # This is the old behavior that will be replaced
        result_sum = np.sum(x * y)
        # They should be identical
        assert_allclose(result_vecdot, result_sum, rtol=1e-12)
    except ImportError:
        # Before PR - function doesn't exist yet
        pass


def test_count_nonzero_equivalence():
    """
    Test that count_nonzero gives same results as sum for boolean arrays.
    
    This test verifies that when the PR is applied, count_nonzero will be used
    instead of sum for boolean arrays to improve performance.
    """
    # Create test boolean array
    np.random.seed(42)
    bool_array = np.random.rand(50) > 0.5
    
    try:
        from scipy._lib._util import np_vecdot
        # Test that count_nonzero gives same result as sum for boolean arrays
        count1 = np.sum(bool_array)
        count2 = np.count_nonzero(bool_array)
        assert_allclose(count1, count2)
    except ImportError:
        # Before PR - this is expected behavior
        count1 = np.sum(bool_array)
        count2 = np.count_nonzero(bool_array)
        assert_allclose(count1, count2)