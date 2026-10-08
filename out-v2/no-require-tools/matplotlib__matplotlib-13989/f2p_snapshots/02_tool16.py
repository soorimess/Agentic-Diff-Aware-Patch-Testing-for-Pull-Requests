"""
Regression test for matplotlib issue where hist() no longer respects range=...
when density=True.

This test ensures that when density=True, the range parameter is still
respected and the bins start at the specified range minimum and end at
the specified range maximum.
"""

import numpy as np
import matplotlib.pyplot as plt


def test_hist_range_with_density():
    """Test that hist() respects range parameter when density=True."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with range and density=True
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should start at 0 and end at 1 when range=(0, 1) is specified
    # and density=True, regardless of the actual data range
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"
    
    # Also test with a different range
    _, bins2, _ = plt.hist(data, "auto", range=(0.2, 0.8), density=True)
    assert bins2[0] == 0.2, f"First bin should be 0.2, got {bins2[0]}"
    assert bins2[-1] == 0.8, f"Last bin should be 0.8, got {bins2[-1]}"


def test_hist_range_with_density_false():
    """Test that hist() respects range parameter when density=False (control test)."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with range and density=False
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=False)
    
    # The bins should start at 0 and end at 1 when range=(0, 1) is specified
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"


def test_hist_density_behavior_preserved():
    """Test that density normalization still works correctly with range."""
    # Create test data that spans a different range than specified
    data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    
    # Test with density=True and range=(0, 1) - should normalize properly
    counts, bins, patches = plt.hist(data, bins=5, range=(0, 1), density=True)
    
    # The area under the histogram should sum to 1 (density=True)
    bin_widths = np.diff(bins)
    total_area = np.sum(counts * bin_widths)
    assert np.isclose(total_area, 1.0), f"Area should be 1.0 for density=True, got {total_area}"
    
    # The bins should respect the range
    assert bins[0] == 0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1, f"Last bin should be 1, got {bins[-1]}"