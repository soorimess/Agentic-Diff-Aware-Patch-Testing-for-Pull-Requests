"""
Regression test for boolean array auto-detection in contour().

This tests that contour() automatically detects boolean arrays and 
defaults to levels=[0.5] for line contours and levels=[0, 0.5, 1] for filled contours.
"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.contour as contour


def test_contour_boolean_autolevels_line():
    """Test that contour with boolean array defaults to levels=[0.5]"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Create contour object directly to test levels 
    fig, ax = plt.subplots()
    try:
        # Test line contour - new behavior for boolean should be [0.5]
        cs = ax.contour(bool_array)
        # Check that levels are [0.5] for boolean arrays (the NEW behavior after PR)
        # This assertion passes on the FIXED version but should fail on OLD version
        expected_levels = [0.5]  
        assert list(cs.levels) == expected_levels, f"Expected {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_contour_boolean_autolevels_filled():
    """Test that contourf with boolean array defaults to levels=[0, 0.5, 1]"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Create contourf object directly to test levels
    fig, ax = plt.subplots()
    try:
        # Test filled contour - new behavior for boolean should be [0, 0.5, 1]
        cs = ax.contourf(bool_array)
        # Check that levels are [0, 0.5, 1] for boolean arrays (the NEW behavior after PR)
        # This assertion passes on the FIXED version but should fail on OLD version
        expected_levels = [0, 0.5, 1]
        assert list(cs.levels) == expected_levels, f"Expected {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_contour_explicit_levels_override():
    """Test that explicit levels still work and override auto-detection"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Create contour object directly to test levels
    fig, ax = plt.subplots()
    try:
        # Test line contour with explicit levels - should override auto-detection
        cs = ax.contour(bool_array, levels=[0.25, 0.75])
        # Should use specified levels, not auto-detected ones
        expected_levels = [0.25, 0.75]
        assert list(cs.levels) == expected_levels, f"Expected {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_contour_regular_float_still_uses_default_behavior():
    """Test that regular float arrays still use default 7 levels behavior (old behavior)"""
    # Create a float 2D array that clearly needs the default auto levels
    float_array = np.random.rand(20, 20)  # bigger array to make it more distinct
    
    # Create contour object directly to test levels  
    fig, ax = plt.subplots()
    try:
        # Test line contour - should still use 7 default levels like before
        cs = ax.contour(float_array)
        # We don't assert the exact count since it's complex behavior,
        # but we ensure that it doesn't fall into the bool behavior
        assert len(cs.levels) >= 1, "Should have at least one level"
        # Should not be [0.5] which would be specifically the boolean case 
        assert list(cs.levels) != [0.5], f"Should not have boolean levels, got {list(cs.levels)}"
    finally:
        plt.close(fig)


def test_contour_boolean_with_explicit_args():
    """Test edge case that boolean detection works in complex contours"""
    # Test a case with more than 1 argument (maybe 3 or 4 args)
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    fig, ax = plt.subplots()
    try:
        # Test how it works when we pass coordinates and arguments
        # This exercises some of the argument parsing paths
        x, y = np.mgrid[0:3, 0:3]
        cs = ax.contour(x, y, bool_array)
        
        # Should still default to [0.5] for boolean case 
        expected_levels = [0.5]
        assert list(cs.levels) == expected_levels, f"Expected {expected_levels}, got {list(cs.levels)}"
    finally:
        plt.close(fig)