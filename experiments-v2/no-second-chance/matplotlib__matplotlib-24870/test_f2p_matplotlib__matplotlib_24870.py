"""
Regression test for matplotlib/matplotlib#24870

Test that boolean arrays passed to contour() automatically get default levels
at 0.5 (or [0, 0.5, 1] for filled contours) instead of the default 7 levels.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import QuadContourSet


def test_contour_boolean_auto_levels_behavior():
    """
    Test that boolean arrays get automatic levels at 0.5 for contour.
    
    Before the fix: boolean array -> 8 levels (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05)
    After the fix: boolean array -> 1 level at 0.5
    """
    # Create a boolean 2D array
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test with matplotlib's contour method
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(z)
        # Check the number of levels - should be 1 with new behavior, 8 with old behavior
        num_levels = len(cs.levels)
        # This test will pass with new behavior (1 level) and fail with old behavior (8 levels)
        # We're asserting that it's the new behavior (1 level)
        assert num_levels == 1, f"Expected 1 level for boolean array, got {num_levels}"
        assert cs.levels[0] == 0.5, f"Expected level at 0.5, got {cs.levels[0]}"
    finally:
        plt.close(fig)


def test_contourf_boolean_auto_levels_behavior():
    """
    Test that boolean arrays get automatic levels at [0, 0.5, 1] for filled_contour.
    
    Before the fix: boolean array -> 8 levels (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05)
    After the fix: boolean array -> 3 levels at [0, 0.5, 1]
    """
    # Create a boolean 2D array
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test with matplotlib's contourf method
    fig, ax = plt.subplots()
    try:
        cs = ax.contourf(z)
        # Check the number of levels - should be 3 with new behavior, 8 with old behavior
        num_levels = len(cs.levels)
        # This test will pass with new behavior (3 levels) and fail with old behavior (8 levels)
        # We're asserting that it's the new behavior (3 levels at [0, 0.5, 1])
        assert num_levels == 3, f"Expected 3 levels for boolean array, got {num_levels}"
        expected_levels = [0.0, 0.5, 1.0]
        assert list(cs.levels) == expected_levels, f"Expected levels {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_non_boolean_still_uses_default_levels():
    """
    Test that non-boolean arrays still use default 7 levels.
    """
    # Create a float 2D array (non-boolean)
    z = np.array([[0.1, 0.3, 0.7],
                  [0.2, 0.6, 0.8],
                  [0.4, 0.5, 0.9]])
    
    # Test with matplotlib's contour method
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(z)
        # Non-boolean arrays should still get default behavior (7 levels)
        num_levels = len(cs.levels)
        # Should have more than 1 level (the old default was 7)
        assert num_levels > 1, f"Expected multiple levels for non-boolean array, got {num_levels}"
    finally:
        plt.close(fig)


def test_explicit_levels_override_auto_detection():
    """
    Test that explicit levels still override auto-detection.
    """
    # Create a boolean 2D array
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test with explicit levels
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(z, levels=[0.2, 0.8])
        # Should use explicit levels, not auto-detected ones
        assert list(cs.levels) == [0.2, 0.8], f"Expected explicit levels [0.2, 0.8], got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_contour_with_x_y_arrays():
    """
    Test contour with explicit x, y arrays to exercise the nargs <= 4 branch.
    """
    # Create test data
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test with matplotlib's contour method using x, y arrays
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(x, y, z)
        # Should work and use auto-detection for boolean array
        # This exercises the nargs <= 4 branch in _contour_args
        assert len(cs.levels) == 1, f"Expected 1 level for boolean array with x,y, got {len(cs.levels)}"
        assert cs.levels[0] == 0.5, f"Expected level at 0.5, got {cs.levels[0]}"
    finally:
        plt.close(fig)


def test_contourf_with_x_y_arrays():
    """
    Test contourf with explicit x, y arrays to exercise the nargs <= 4 branch.
    """
    # Create test data
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Test with matplotlib's contourf method using x, y arrays
    fig, ax = plt.subplots()
    try:
        cs = ax.contourf(x, y, z)
        # Should work and use auto-detection for boolean array
        # This exercises the nargs <= 4 branch in _contour_args
        assert len(cs.levels) == 3, f"Expected 3 levels for boolean array with x,y, got {len(cs.levels)}"
        expected_levels = [0.0, 0.5, 1.0]
        assert list(cs.levels) == expected_levels, f"Expected levels {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)