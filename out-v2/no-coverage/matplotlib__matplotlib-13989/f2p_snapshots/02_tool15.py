import numpy as np
import matplotlib.pyplot as plt


def test_hist_range_with_density():
    """Test that hist() respects range=... when density=True"""
    # This is the exact example from the bug report
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=True)
    
    # The bins should respect the specified range
    # First bin should be 0 and last bin should be 1
    assert bins[0] == 0.0
    assert bins[-1] == 1.0


def test_hist_range_with_density_false():
    """Test that hist() respects range=... when density=False (control test)"""
    # This should work correctly (density=False)
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=False)
    
    # The bins should respect the specified range
    assert bins[0] == 0.0
    assert bins[-1] == 1.0