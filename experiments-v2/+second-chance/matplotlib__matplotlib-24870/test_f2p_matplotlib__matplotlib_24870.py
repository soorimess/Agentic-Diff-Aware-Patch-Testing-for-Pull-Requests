"""
Regression test for auto-detection of boolean arrays in contour().

This test ensures that boolean arrays passed to contour() and contourf()
automatically get default levels appropriate for boolean data:
- contour(boolean_array) should default to levels=[0.5]
- contourf(boolean_array) should default to levels=[0, 0.5, 1]
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.contour as contour_module
from matplotlib.testing.decorators import image_comparison


def test_contour_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and appropriate default levels."""
    # Create a simple boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with boolean array - should default to levels=[0.5]
    fig, ax = plt.subplots()
    contour_set = ax.contour(data)
    
    # Check that the levels are [0.5] (not the default 7 levels)
    expected_levels = [0.5]
    actual_levels = contour_set.levels.tolist()
    
    # The old behavior would have used 7 levels, the new behavior uses 1 level at 0.5
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contourf_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and appropriate default levels for filled contours."""
    # Create a simple boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf with boolean array - should default to levels=[0, 0.5, 1]
    fig, ax = plt.subplots()
    contour_set = ax.contourf(data)
    
    # Check that the levels are [0, 0.5, 1] (not the default 7 levels)
    expected_levels = [0.0, 0.5, 1.0]
    actual_levels = contour_set.levels.tolist()
    
    # The old behavior would have used 7 levels, the new behavior uses 3 levels [0, 0.5, 1]
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contour_non_boolean_still_works():
    """Test that non-boolean arrays still work as before."""
    # Create a regular float 2D array
    data = np.array([[1.0, 2.0, 3.0],
                     [2.0, 3.0, 4.0],
                     [3.0, 4.0, 5.0]])
    
    # Test contour with regular float array - should still default to 7 levels
    fig, ax = plt.subplots()
    contour_set = ax.contour(data)
    
    # Check that the levels are the default 7 levels (not 1 level)
    # The actual levels depend on the data range, but should be more than 1
    assert len(contour_set.levels) > 1, "Non-boolean arrays should still get multiple default levels"
    
    plt.close(fig)


def test_contourf_non_boolean_still_works():
    """Test that non-boolean arrays still work as before for filled contours."""
    # Create a regular float 2D array
    data = np.array([[1.0, 2.0, 3.0],
                     [2.0, 3.0, 4.0],
                     [3.0, 4.0, 5.0]])
    
    # Test contourf with regular float array - should still default to 7 levels
    fig, ax = plt.subplots()
    contour_set = ax.contourf(data)
    
    # Check that the levels are the default 7 levels (not 1 level)
    # The actual levels depend on the data range, but should be more than 1
    assert len(contour_set.levels) > 1, "Non-boolean arrays should still get multiple default levels"
    
    plt.close(fig)


def test_contour_explicit_levels_override():
    """Test that explicit levels still override the auto-detection."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with boolean array but explicit levels
    fig, ax = plt.subplots()
    contour_set = ax.contour(data, levels=[0.25, 0.75])
    
    # Check that the levels are the explicit ones
    expected_levels = [0.25, 0.75]
    actual_levels = contour_set.levels.tolist()
    
    assert actual_levels == expected_levels, f"Expected explicit levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contourf_explicit_levels_override():
    """Test that explicit levels still override the auto-detection for filled contours."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf with boolean array but explicit levels
    fig, ax = plt.subplots()
    contour_set = ax.contourf(data, levels=[0.1, 0.5, 0.9])
    
    # Check that the levels are the explicit ones
    expected_levels = [0.1, 0.5, 0.9]
    actual_levels = contour_set.levels.tolist()
    
    assert actual_levels == expected_levels, f"Expected explicit levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contour_with_3d_args():
    """Test contour with 3D arguments (x, y, z) - should exercise new argument handling."""
    # Create coordinate arrays and a boolean 2D array
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 3)
    X, Y = np.meshgrid(x, y)
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with 3D args - should default to levels=[0.5]
    fig, ax = plt.subplots()
    contour_set = ax.contour(X, Y, data)
    
    # Check that the levels are [0.5] (not the default 7 levels)
    expected_levels = [0.5]
    actual_levels = contour_set.levels.tolist()
    
    # The old behavior would have used 7 levels, the new behavior uses 1 level at 0.5
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)


def test_contourf_with_3d_args():
    """Test contourf with 3D arguments (x, y, z) - should exercise new argument handling."""
    # Create coordinate arrays and a boolean 2D array
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 3)
    X, Y = np.meshgrid(x, y)
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf with 3D args - should default to levels=[0, 0.5, 1]
    fig, ax = plt.subplots()
    contour_set = ax.contourf(X, Y, data)
    
    # Check that the levels are [0, 0.5, 1] (not the default 7 levels)
    expected_levels = [0.0, 0.5, 1.0]
    actual_levels = contour_set.levels.tolist()
    
    # The old behavior would have used 7 levels, the new behavior uses 3 levels [0, 0.5, 1]
    assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
    
    plt.close(fig)