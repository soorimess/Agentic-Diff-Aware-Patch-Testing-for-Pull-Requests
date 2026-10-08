import numpy as np
import matplotlib.pyplot as plt
import pytest


def test_hist_range_density():
    """Test that hist() respects range=... when density=True."""
    # Reproduce the exact example from the bug report
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    # First bin edge should be 0, last bin edge should be 1
    # Using a more lenient tolerance since we're dealing with random data
    assert bins[0] == 0.0, f"Expected first bin to be 0.0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Expected last bin to be 1.0, got {bins[-1]}"


def test_hist_range_density_false():
    """Test that hist() respects range=... when density=False (should work)."""
    # Reproduce the exact example from the bug report
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=False)
    
    # The bins should respect the specified range
    # First bin edge should be 0, last bin edge should be 1
    assert bins[0] == 0.0
    assert bins[-1] == 1.0