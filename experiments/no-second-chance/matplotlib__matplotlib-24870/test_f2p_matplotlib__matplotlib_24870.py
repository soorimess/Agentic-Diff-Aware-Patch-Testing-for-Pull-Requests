"""
Test for regression of boolean array auto-detection in contour().

This test ensures that when boolean arrays are passed to contour(),
they automatically get levels=[0.5] for contour lines and 
levels=[0, 0.5, 1] for filled contours, instead of the default 7 levels.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_contour_boolean_auto_levels_contour_lines():
    """Test that boolean arrays get default level [0.5] for contour lines."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Create a contour plot - should auto-detect boolean and use levels=[0.5]
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Check that we get the expected [0.5] level instead of default 8+ levels
    # Before fix: should have 8 default levels: [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05] 
    # After fix: should have 1 level: [0.5]
    assert len(cs.levels) == 1, f"Expected 1 level for boolean contour, got {len(cs.levels)} levels"
    assert cs.levels[0] == 0.5, f"Expected level 0.5, got {cs.levels[0]}"
    
    plt.close(fig)


def test_contour_boolean_auto_levels_filled_contours():
    """Test that boolean arrays get default levels [0, 0.5, 1] for filled contours."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Create a filled contour plot - should auto-detect boolean and use levels=[0, 0.5, 1]
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # Check that we get the expected [0, 0.5, 1] levels instead of default 8+ levels  
    # Before fix: should have 8 default levels: [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05]
    # After fix: should have 3 levels: [0, 0.5, 1]
    assert len(cs.levels) == 3, f"Expected 3 levels for boolean filled contour, got {len(cs.levels)} levels"
    expected_levels = [0, 0.5, 1]
    for i, expected in enumerate(expected_levels):
        assert cs.levels[i] == expected, f"Level {i}: expected {expected}, got {cs.levels[i]}"
    
    plt.close(fig)


def test_contour_boolean_different_values():
    """Test that boolean arrays with different True/False patterns still work."""
    # Create another boolean array
    data = np.array([[True, True, False, False],
                     [True, True, False, False],
                     [False, False, True, True],
                     [False, False, True, True]])
    
    # Test contour lines
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    assert len(cs.levels) == 1
    assert cs.levels[0] == 0.5
    plt.close(fig)
    
    # Test filled contours
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    assert len(cs.levels) == 3
    expected_levels = [0, 0.5, 1]
    for i, expected in enumerate(expected_levels):
        assert cs.levels[i] == expected
    plt.close(fig)


def test_contour_3d_args_boolean():
    """Test 3-argument case with boolean array (x, y, z) - covers missing code path."""
    # Create coordinate arrays
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 2, 3) 
    X, Y = np.meshgrid(x, y)
    
    # Create boolean data
    Z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test contour lines with 3 args
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, Z)
    assert len(cs.levels) == 1
    assert cs.levels[0] == 0.5
    plt.close(fig)
    
    # Test filled contours with 3 args
    fig, ax = plt.subplots()
    cs = ax.contourf(X, Y, Z)
    assert len(cs.levels) == 3
    expected_levels = [0, 0.5, 1]
    for i, expected in enumerate(expected_levels):
        assert cs.levels[i] == expected
    plt.close(fig)


def test_contour_non_boolean_still_works():
    """Test that non-boolean arrays still behave as before (default 7 levels)."""
    # Create a float array 
    data = np.array([[0.1, 0.3, 0.7],
                     [0.2, 0.5, 0.8],
                     [0.4, 0.6, 0.9]])
    
    # Test contour lines - should get default 7 levels (not 1 level at 0.5)
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    # Should have 8 levels from default behavior (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05)
    # This verifies the main branch is still working correctly  
    assert len(cs.levels) >= 2  # At least 2 levels, but we don't want exactly 1 (that's boolean case)
    plt.close(fig)
    
    # Test filled contours - should get default 7 levels
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    # Should have 8 levels from default behavior (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05)
    assert len(cs.levels) >= 2  # At least 2 levels, but we don't want exactly 3 (that's boolean case)
    plt.close(fig)