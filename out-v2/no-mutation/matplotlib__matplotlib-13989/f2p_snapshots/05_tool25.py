"""
Regression test for matplotlib issue #13989.

When hist() is called with density=True and range=...,
the range parameter should be respected.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_hist_density_respects_range_exact_bug_report():
    """Test the exact case from the bug report."""
    # This is the exact code from the bug report
    np.random.seed(42)  # For reproducibility to match expected output
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=True)
    
    # Before fix: bins would be [0.00331535 0.18930174 0.37528813 0.56127453 0.74726092 0.93324731]
    # After fix: bins should start at 0 and end at 1
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # The original bug showed that first bin was 0.00331535 instead of 0
    # So we're testing that it's now fixed
    expected_first = 0.0
    expected_last = 1.0
    assert bins[0] == expected_first, f"Expected first bin to be {expected_first}, got {bins[0]}"
    assert bins[-1] == expected_last, f"Expected last bin to be {expected_last}, got {bins[-1]}"


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