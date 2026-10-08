"""
Regression test for matplotlib bug where hist() no longer respects range=...
when density=True.

This test ensures that when density=True and range is specified, the
returned bins array has the correct range bounds.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_hist_range_density():
    """Test that hist respects range parameter when density=True."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with density=True and a specific range
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should start at 0 and end at 1 when range=(0, 1) is specified
    # and density=True is used
    assert bins[0] == 0.0, f"Expected first bin to be 0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Expected last bin to be 1, got {bins[-1]}"
    
    # Additional check: bins should span the full range
    expected_range = 1.0 - 0.0  # 1.0
    actual_range = bins[-1] - bins[0]
    assert actual_range == expected_range, f"Expected range {expected_range}, got {actual_range}"


def test_hist_range_no_density():
    """Test that hist still respects range parameter when density=False."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with density=False and a specific range - this should work correctly
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=False)
    
    # The bins should start at 0 and end at 1 when range=(0, 1) is specified
    assert bins[0] == 0.0, f"Expected first bin to be 0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Expected last bin to be 1, got {bins[-1]}"