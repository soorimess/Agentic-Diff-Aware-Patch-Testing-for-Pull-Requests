"""
Regression test for matplotlib bug where hist() no longer respects range=...
when density=True.

This test ensures that when density=True, the range parameter is still
properly respected and the bins array has the correct bounds.
"""

import numpy as np
import matplotlib.pyplot as plt
import pytest


def test_hist_range_with_density():
    """Test that hist() respects range parameter when density=True."""
    # Create test data that fits within range (0, 1)
    np.random.seed(12345)
    data = np.random.rand(10)
    
    # Test with density=True and range=(0, 1)
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins=5, range=(0, 1), density=True)
    
    # The bins should start at 0 and end at 1 when range is specified
    # and density=True, because the histogram is normalized to integrate to 1
    # over the specified range
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Clean up
    plt.close(fig)


def test_hist_range_with_density_and_auto_bins():
    """Test that hist() respects range parameter when density=True with auto bins."""
    # Create test data that fits within range (0, 1)
    np.random.seed(12345)
    data = np.random.rand(10)
    
    # Test with density=True, auto bins, and range=(0, 1)
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should start at 0 and end at 1 when range is specified
    # and density=True
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Clean up
    plt.close(fig)


def test_hist_range_without_density():
    """Test that hist() respects range parameter when density=False (control test)."""
    # Create test data that fits within range (0, 1)
    np.random.seed(12345)
    data = np.random.rand(10)
    
    # Test with density=False and range=(0, 1)
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins=5, range=(0, 1), density=False)
    
    # The bins should start at 0 and end at 1 when range is specified
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Clean up
    plt.close(fig)