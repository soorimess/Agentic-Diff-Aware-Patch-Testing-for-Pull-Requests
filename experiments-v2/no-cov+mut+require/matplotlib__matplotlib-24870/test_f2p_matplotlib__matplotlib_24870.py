"""
Test for auto-detection of boolean arrays in contour().

This test ensures that boolean 2D arrays passed to contour() automatically
default to levels=[0.5] (for contour) or levels=[0, 0.5, 1] (for contourf)
instead of the default 7 levels.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet


def test_contour_boolean_auto_levels():
    """Test that boolean arrays get automatic level detection."""
    # Create a boolean 2D array
    np.random.seed(42)
    bool_array = np.random.rand(10, 10) > 0.5
    
    # Test contour (not filled) - should auto-detect and use [0.5]
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array)
    
    # Check that levels are [0.5] instead of default 7 levels
    expected_levels = [0.5]
    assert cs.levels.tolist() == expected_levels, f"Expected levels {expected_levels}, got {cs.levels.tolist()}"
    plt.close(fig)
    
    # Test contourf (filled) - should auto-detect and use [0, 0.5, 1]
    fig, ax = plt.subplots()
    cs = ax.contourf(bool_array)
    
    # Check that levels are [0, 0.5, 1] instead of default 7 levels
    expected_levels = [0.0, 0.5, 1.0]
    assert cs.levels.tolist() == expected_levels, f"Expected levels {expected_levels}, got {cs.levels.tolist()}"
    plt.close(fig)


def test_contour_boolean_explicit_levels():
    """Test that explicit levels still work for boolean arrays."""
    # Create a boolean 2D array
    np.random.seed(42)
    bool_array = np.random.rand(10, 10) > 0.5
    
    # Test contour with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array, levels=[0.2, 0.8])
    
    # Check that explicit levels are respected
    expected_levels = [0.2, 0.8]
    assert cs.levels.tolist() == expected_levels, f"Expected levels {expected_levels}, got {cs.levels.tolist()}"
    plt.close(fig)
    
    # Test contourf with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contourf(bool_array, levels=[0.1, 0.5, 0.9])
    
    # Check that explicit levels are respected
    expected_levels = [0.1, 0.5, 0.9]
    assert cs.levels.tolist() == expected_levels, f"Expected levels {expected_levels}, got {cs.levels.tolist()}"
    plt.close(fig)


def test_contour_non_boolean_still_works():
    """Test that non-boolean arrays still work normally."""
    # Create a regular float 2D array
    np.random.seed(42)
    float_array = np.random.rand(10, 10)
    
    # Test contour - should work normally
    fig, ax = plt.subplots()
    cs = ax.contour(float_array)
    
    # Check that we get some levels (not the boolean auto-detection)
    assert len(cs.levels) > 1, f"Expected multiple levels, got {len(cs.levels)}"
    plt.close(fig)
    
    # Test contourf - should work normally
    fig, ax = plt.subplots()
    cs = ax.contourf(float_array)
    
    # Check that we get some levels (not the boolean auto-detection)
    assert len(cs.levels) > 1, f"Expected multiple levels, got {len(cs.levels)}"
    plt.close(fig)