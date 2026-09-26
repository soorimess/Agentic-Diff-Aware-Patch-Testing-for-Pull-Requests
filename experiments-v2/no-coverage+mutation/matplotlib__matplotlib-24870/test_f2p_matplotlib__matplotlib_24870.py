"""
Regression test for boolean array auto-detection in contour().

This test ensures that boolean 2D arrays passed to contour() and contourf()
automatically get default levels at 0.5 (or [0, 0.5, 1] for filled contours),
rather than the default 7 levels that would be used for other data types.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet


def test_contour_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and use appropriate default levels."""
    # Create a simple boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour (non-filled) - should default to [0.5]
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Check that levels are [0.5] not the default 7 levels
    expected_levels = [0.5]
    actual_levels = cs.levels.tolist()
    
    # The old behavior would use 7 default levels, the new behavior uses [0.5]
    # We're testing that the new behavior is working
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contourf_boolean_auto_levels():
    """Test that boolean arrays passed to contourf() get appropriate default levels."""
    # Create a simple boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf (filled) - should default to [0, 0.5, 1]
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # Check that levels are [0, 0.5, 1] not the default 7 levels
    expected_levels = [0.0, 0.5, 1.0]
    actual_levels = cs.levels.tolist()
    
    # The old behavior would use 7 default levels, the new behavior uses [0, 0.5, 1]
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contour_non_boolean_still_works():
    """Test that non-boolean arrays still work as before."""
    # Create a regular float 2D array
    data = np.array([[1.0, 2.0, 3.0],
                     [2.0, 3.0, 4.0],
                     [3.0, 4.0, 5.0]])
    
    # Test contour - should still default to levels based on data range
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Check that we get levels based on the data range (not 7 levels)
    # The actual values depend on the data range, but should be more than 7
    # In this case we get 9 levels from 1.0 to 5.0 in steps of 0.5
    assert len(cs.levels) >= 7, f"Expected at least 7 levels, got {len(cs.levels)}"
    
    plt.close(fig)