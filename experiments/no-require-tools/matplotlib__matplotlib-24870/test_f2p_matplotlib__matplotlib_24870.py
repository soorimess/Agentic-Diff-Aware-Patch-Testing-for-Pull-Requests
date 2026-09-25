"""
Regression test for matplotlib bug #24870: Auto-detect bool arrays passed to contour()

This test verifies that boolean 2D arrays passed to contour() automatically
get default levels set to [0.5] instead of the default 8 levels.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

def test_contour_bool_array_auto_levels():
    """Test that boolean arrays in contour() get auto-detected levels [0.5]."""
    # Create a simple boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with bool array (should auto-detect and use [0.5])
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array)
    
    # For a boolean array in contour (filled=False), the default levels should be [0.5]
    levels = cs.levels
    assert len(levels) == 1
    assert levels[0] == 0.5
    plt.close(fig)

def test_contourf_bool_array_auto_levels():
    """Test that boolean arrays in contourf() get auto-detected levels [0, 0.5, 1]."""
    # Create a simple boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contourf with bool array (should auto-detect and use [0, 0.5, 1])
    fig, ax = plt.subplots() 
    cs = ax.contourf(bool_array)
    
    # For a boolean array in contourf (filled=True), the default levels should be [0, 0.5, 1]
    levels = cs.levels
    assert len(levels) == 3
    assert levels[0] == 0
    assert levels[1] == 0.5
    assert levels[2] == 1.0
    plt.close(fig)

def test_contour_with_coordinate_arrays():
    """Test that boolean arrays work correctly when x, y coordinates are also specified."""
    # Create test arrays
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 2, 3)
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with explicit x, y arrays and bool array
    fig, ax = plt.subplots()
    cs = ax.contour(x, y, bool_array)
    
    # Should still get auto-detected [0.5] levels
    levels = cs.levels
    assert len(levels) == 1
    assert levels[0] == 0.5
    plt.close(fig)

def test_contourf_with_coordinate_arrays():
    """Test that boolean arrays work correctly with contourf when x, y coordinates are also specified."""
    # Create test arrays
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 2, 3)
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contourf with explicit x, y arrays and bool array
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, bool_array)
    
    # Should still get auto-detected [0, 0.5, 1] levels
    levels = cs.levels
    assert len(levels) == 3
    assert levels[0] == 0
    assert levels[1] == 0.5
    assert levels[2] == 1.0
    plt.close(fig)

def test_contour_non_bool_array_still_default():
    """Test that non-boolean arrays still get the default behavior."""
    # Create a regular 2D float array
    float_array = np.array([[1.0, 2.0, 3.0],
                           [2.0, 3.0, 4.0],
                           [3.0, 4.0, 5.0]])
    
    # Test contour with regular float array
    fig, ax = plt.subplots()
    cs = ax.contour(float_array)
    
    # Non-boolean arrays should still get default behavior 
    # (but not the specific 1 or 3 level behavior we're testing for)
    levels = cs.levels
    assert len(levels) > 1
    # This is just verifying it's not a boolean case
    assert not all(level in [0, 0.5, 1] for level in levels)
    plt.close(fig)

def test_contour_explicit_levels_still_work():
    """Test that explicitly set levels still work correctly."""
    # Create a boolean array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with explicit levels (should use provided levels regardless)
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array, levels=[0.2, 0.8])
    
    # The levels should be the explicitly specified ones
    levels = cs.levels
    assert len(levels) == 2
    assert levels[0] == 0.2
    assert levels[1] == 0.8
    plt.close(fig)