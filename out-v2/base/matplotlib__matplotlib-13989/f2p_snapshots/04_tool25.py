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
    
    # The actual bin edges should be within the specified range
    assert bins[0] >= 0, f"First bin should be >= 0, got {bins[0]}"
    assert bins[-1] <= 1, f"Last bin should be <= 1, got {bins[-1]}"
    
    # More comprehensive check - bins should span the full range
    expected_bins = np.linspace(0, 1, 6)  # 5 bins = 6 edges
    # Check that the bins are properly distributed within the range
    assert len(bins) == 6, f"Expected 6 bin edges for 5 bins, got {len(bins)}"
    
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


def test_hist_range_with_density_and_stacked():
    """Test that hist() respects range parameter when density=True and stacked=True."""
    # Create test data that fits within range (0, 1)
    np.random.seed(12345)
    data1 = np.random.rand(10)
    data2 = np.random.rand(10)
    
    # Test with density=True, stacked=True, and range=(0, 1)
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist([data1, data2], bins=5, range=(0, 1), density=True, stacked=True)
    
    # The bins should start at 0 and end at 1 when range is specified
    # and density=True, even with stacked=True
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Clean up
    plt.close(fig)


def test_hist_range_preservation_independent_of_density_value():
    """Test that range is preserved regardless of density value being truthy or falsy."""
    # Create test data that fits within range (0, 1)
    np.random.seed(12345)
    data = np.random.rand(10)
    
    # Test with density=False (falsy) and range=(0, 1)
    fig1, ax1 = plt.subplots()
    n1, bins1, patches1 = ax1.hist(data, bins=5, range=(0, 1), density=False)
    
    # Test with density=True (truthy) and range=(0, 1)  
    fig2, ax2 = plt.subplots()
    n2, bins2, patches2 = ax2.hist(data, bins=5, range=(0, 1), density=True)
    
    # Both should have the same bin structure
    assert np.array_equal(bins1, bins2), "Bins should be identical regardless of density value"
    
    # Both should respect the range
    assert bins1[0] == 0 and bins1[-1] == 1, "First and last bins should respect range with density=False"
    assert bins2[0] == 0 and bins2[-1] == 1, "First and last bins should respect range with density=True"
    
    # Clean up
    plt.close(fig1)
    plt.close(fig2)