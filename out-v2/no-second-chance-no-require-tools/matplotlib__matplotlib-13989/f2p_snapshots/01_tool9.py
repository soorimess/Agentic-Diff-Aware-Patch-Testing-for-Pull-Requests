"""
Regression test for matplotlib issue #13989.

hist() no longer respects range=... when density=True
"""
import numpy as np
import matplotlib.pyplot as plt


def test_hist_range_with_density():
    """Test that hist() respects range parameter when density=True."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with density=True and explicit range
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    # First bin should be 0, last bin should be 1
    assert bins[0] == 0.0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Last bin should be 1, got {bins[-1]}"
    

def test_hist_range_with_density_false():
    """Test that hist() respects range parameter when density=False (should work)."""
    # Create test data
    data = np.random.rand(10)
    
    # Call hist with density=False and explicit range
    _, bins, _ = plt.hist(data, "auto", range=(0, 1), density=False)
    
    # The bins should respect the specified range
    # First bin should be 0, last bin should be 1
    assert bins[0] == 0.0, f"First bin should be 0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Last bin should be 1, got {bins[-1]}"