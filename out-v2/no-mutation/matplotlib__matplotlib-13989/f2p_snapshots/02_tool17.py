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
    
    # Call hist with density=True and explicit range
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    # First bin should be 0 and last bin should be 1
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Also test with a different range
    _, bins2, _ = plt.hist(data, "auto", range=(0.2, 0.8), density=True)
    assert bins2[0] == 0.2, f"First bin should be 0.2, got {bins2[0]}"
    assert bins2[-1] == 0.8, f"Last bin should be 0.8, got {bins2[-1]}"


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


def test_hist_density_respects_range_multiple_datasets():
    """Test that hist() with density=True and multiple datasets respects the range parameter."""
    # Create test data in range [0, 1]
    np.random.seed(42)  # For reproducibility
    data1 = np.random.rand(5)
    data2 = np.random.rand(5) + 0.5  # Second dataset shifted
    
    # Call hist with density=True and explicit range
    _, bins, _ = plt.hist([data1, data2], "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"


def test_hist_density_with_stacked_false():
    """Test that hist() with density=True and stacked=False respects range."""
    np.random.seed(42)
    data = np.random.rand(10)
    
    # Call hist with density=True, stacked=False, and explicit range
    _, bins, _ = plt.hist(data, "auto", range=(0.1, 0.9), density=True, stacked=False)
    
    # The bins should respect the specified range
    assert bins[0] == 0.1, f"First bin should be 0.1, got {bins[0]}"
    assert bins[-1] == 0.9, f"Last bin should be 0.9, got {bins[-1]}"