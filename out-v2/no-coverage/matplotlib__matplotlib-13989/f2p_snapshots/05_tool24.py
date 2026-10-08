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


def test_hist_density_parameter_is_respected():
    """Test that density parameter actually affects histogram behavior"""
    # Create test data where we can clearly see the difference between density=True and False
    data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    
    # Test with density=True - values should be normalized
    n1, bins1, _ = plt.hist(data, bins=3, range=(0, 1), density=True)
    
    # Test with density=False - values should be raw counts
    n2, bins2, _ = plt.hist(data, bins=3, range=(0, 1), density=False)
    
    # The bins should be the same in both cases
    np.testing.assert_array_equal(bins1, bins2)
    
    # The values should be different (density=True normalizes)
    assert not np.array_equal(n1, n2)
    
    # With density=True, the first bin should start at 0 and end at 0.333... with range=(0,1) and 3 bins
    assert bins1[0] == 0.0
    assert bins1[-1] == 1.0