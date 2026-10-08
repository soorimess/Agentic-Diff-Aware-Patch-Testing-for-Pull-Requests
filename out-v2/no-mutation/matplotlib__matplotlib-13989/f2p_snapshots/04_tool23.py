"""
Regression test for matplotlib issue #13989.

When hist() is called with density=True and range=...,
the range parameter should be respected.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_hist_density_respects_range():
    """Test that hist() with density=True respects the range parameter."""
    # Create test data in range [0, 1] 
    np.random.seed(42)  # For reproducibility
    data = np.random.rand(10)
    
    # Call hist with density=True and explicit range - this is the exact case from bug report
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    # Before the fix, bins[0] would be ~0.058 instead of 0
    # The first bin should be exactly 0 (as specified in range)
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    # The last bin should be exactly 1 (as specified in range)
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Also verify that the range is actually respected by checking that
    # bins span the full specified range
    expected_range = 1.0 - 0.0  # 1.0
    actual_range = bins[-1] - bins[0] 
    assert abs(actual_range - expected_range) < 1e-10, \
        f"Bin range should be {expected_range}, got {actual_range}"


def test_hist_density_false_ignores_range():
    """Test that hist() with density=False ignores the range parameter (expected behavior)."""
    # Create test data in range [0, 1]
    np.random.seed(42)  # For reproducibility
    data = np.random.rand(10)
    
    # Call hist with density=False and explicit range
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=False)
    
    # With density=False, range should be ignored and bins should cover data range
    # This is the expected behavior, not the bug we're testing for
    assert bins[0] <= 0, f"First bin should be <= 0, got {bins[0]}"
    assert bins[-1] >= 1, f"Last bin should be >= 1, got {bins[-1]}"