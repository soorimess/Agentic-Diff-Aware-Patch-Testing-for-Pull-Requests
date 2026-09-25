"""
Regression test for boolean array auto-detection in contour().

This test ensures that when contour() is called with a boolean 2D array
without explicit levels, it automatically uses [0.5] as levels rather than 
the default 7 levels which would result in overlapping contours.
"""

import numpy as np
import matplotlib.pyplot as plt


def test_contour_boolean_auto_levels():
    """Test that boolean arrays automatically use levels=[0.5]"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False], 
                          [True, False, True]])
    
    # Create a figure and axis for testing
    fig, ax = plt.subplots()
    
    # Call contour with boolean array (no explicit levels)
    # Before fix: this should use 7 default levels from 0 to 1.05
    # After fix: this should use [0.5] levels
    cs = ax.contour(bool_array)
    
    # The levels should be [0.5] for boolean arrays, not the default 7 levels
    actual_levels = cs.levels
    
    # Should get 1 level (0.5) instead of 7+ levels for boolean input
    assert len(actual_levels) == 1, f"Expected 1 level for boolean array, got {len(actual_levels)}"
    assert actual_levels[0] == 0.5, f"Expected level 0.5, got {actual_levels[0]}"
    
    plt.close(fig)


def test_contourf_boolean_auto_levels():
    """Test that boolean arrays automatically use levels=[0, 0.5, 1] for filled contours"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False], 
                          [True, False, True]])
    
    # Create a figure and axis for testing
    fig, ax = plt.subplots()
    
    # Call contourf with boolean array (no explicit levels)
    # Before fix: this would use 7 default levels from 0 to 1.05  
    # After fix: this should use [0, 0.5, 1] levels
    cs = ax.contourf(bool_array)
    
    # For filled contours with boolean data, the levels should be [0, 0.5, 1]
    actual_levels = cs.levels
    
    # Should get 3 levels (0, 0.5, 1) instead of 7+ levels for boolean input
    assert len(actual_levels) == 3, f"Expected 3 levels for filled boolean array, got {len(actual_levels)}"
    assert actual_levels[0] == 0, f"Expected first level 0, got {actual_levels[0]}"
    assert actual_levels[1] == 0.5, f"Expected middle level 0.5, got {actual_levels[1]}"
    assert actual_levels[2] == 1, f"Expected last level 1, got {actual_levels[2]}"
    
    plt.close(fig)


def test_contour_boolean_explicit_levels_override():
    """Test that explicit levels still override the automatic detection"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False], 
                          [True, False, True]])
    
    # Create a figure and axis for testing
    fig, ax = plt.subplots()
    
    # Call contour with boolean array but explicit levels
    # Should still use the explicit levels, not auto-detect
    cs = ax.contour(bool_array, levels=[0.2, 0.8])
    
    # The levels should be the explicitly provided levels
    actual_levels = cs.levels
    
    assert len(actual_levels) == 2, f"Expected 2 explicit levels, got {len(actual_levels)}"
    assert actual_levels[0] == 0.2, f"Expected first level 0.2, got {actual_levels[0]}"
    assert actual_levels[1] == 0.8, f"Expected second level 0.8, got {actual_levels[1]}"
    
    plt.close(fig)