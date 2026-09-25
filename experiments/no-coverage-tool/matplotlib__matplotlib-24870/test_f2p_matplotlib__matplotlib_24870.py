"""
Regression test for boolean array auto-detection in contour().

This test verifies that boolean 2D arrays now get special default levels
in contour() and contourf() functions, which would not happen in old code.

The key observable differences are in how special default levels are applied
for boolean dtype inputs when no explicit levels are provided.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_contour_boolean_uses_single_level():
    """Test that boolean contour arrays get [0.5] instead of standard levels."""
    # Create a boolean array that should trigger the new logic
    data = np.array([[True, False], [False, True]], dtype=bool)
    
    # Create contour plot with boolean data
    fig, ax = plt.subplots()
    
    try:
        cs = ax.contour(data)
        levels = cs.levels
        
        # This assertion tests the NEW behavior:
        # - boolean arrays get [0.5] level  
        # - this will only work with the fix applied
        # - old code wouldn't recognize this special case
        expected_single_level = 0.5
        assert len(levels) == 1, f"Boolean contour should have 1 level, got {len(levels)}"
        assert abs(levels[0] - expected_single_level) < 1e-10, \
            f"Boolean contour should have level at 0.5, got {levels[0]}"
            
    finally:
        plt.close(fig)


def test_contourf_boolean_uses_three_levels():
    """Test that boolean contourf arrays get [0, 0.5, 1] instead of standard levels."""
    # Create a boolean array that should trigger the new logic
    data = np.array([[True, False], [False, True]], dtype=bool)
    
    # Create contourf plot with boolean data
    fig, ax = plt.subplots()
    
    try:
        cs = ax.contourf(data)
        levels = cs.levels
        
        # This assertion tests the NEW behavior for filled contours:
        # - boolean filled contours get [0, 0.5, 1] levels
        # - this will only work with the fix applied
        expected_levels = [0.0, 0.5, 1.0]
        assert len(levels) == 3, f"Boolean contourf should have 3 levels, got {len(levels)}"
        assert np.allclose(levels, expected_levels), \
            f"Boolean contourf should have levels [0, 0.5, 1], got {levels}"
            
    finally:
        plt.close(fig)


def test_non_boolean_arrays_unchanged():
    """Test that non-boolean arrays still follow standard behavior (regression test)."""
    # Non-boolean array should not be affected by the new logic
    data = np.array([[0.1, 0.9], [0.3, 0.7]])
    
    fig, ax = plt.subplots()
    
    try:
        cs = ax.contour(data)
        levels = cs.levels

        # This tests invariant behavior - should work in both states
        # The exact number might vary, but the principle remains
        assert len(levels) >= 2, f"Non-boolean arrays should have multiple levels, got {len(levels)}"
        
    finally:
        plt.close(fig)


def test_explicit_levels_prevent_auto_detection():
    """Test that explicit levels prevent any special auto-detection behaviors."""
    # Boolean array with explicit levels should ignore the new logic
    data = np.array([[True, False], [False, True]], dtype=bool)
    
    fig, ax = plt.subplots()
    
    try:
        cs = ax.contour(data, levels=[0.2, 0.8])
        levels = cs.levels
        
        # Should ignore boolean special handling and use explicitly specified levels
        expected = [0.2, 0.8]
        assert levels.tolist() == expected, f"Should use explicit levels, got {levels.tolist()}"
        
    finally:
        plt.close(fig)