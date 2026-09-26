"""
Regression tests for boolean array auto-detection in contour().

This test verifies that boolean 2D arrays passed to contour() and contourf()
automatically get default levels at 0.5 (for contour) or [0, 0.5, 1] (for contourf)
instead of the default 7 levels.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet
from numpy.testing import assert_array_almost_equal


def test_contour_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and use [0.5] levels."""
    # Create a boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10) > 0.5
    
    # Test contour with boolean array - should get [0.5] levels with new behavior
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # With the fix applied, this should be 1 level [0.5]
    # With old behavior, this would be 8 default levels
    actual_levels = cs.levels
    
    # This test should FAIL with current code (old behavior) and PASS with new behavior
    assert len(actual_levels) == 1, f"Expected 1 level for boolean contour, got {len(actual_levels)}"
    assert actual_levels[0] == 0.5, f"Expected level 0.5, got {actual_levels[0]}"
    
    plt.close(fig)


def test_contourf_boolean_auto_levels():
    """Test that boolean arrays passed to contourf() get [0, 0.5, 1] levels."""
    # Create a boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10) > 0.5
    
    # Test contourf with boolean array - should get [0, 0.5, 1] levels with new behavior
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # With the fix applied, this should be 3 levels [0, 0.5, 1]
    # With old behavior, this would be 8 default levels
    actual_levels = cs.levels
    
    # This test should FAIL with current code (old behavior) and PASS with new behavior
    assert len(actual_levels) == 3, f"Expected 3 levels for boolean contourf, got {len(actual_levels)}"
    expected_levels = [0.0, 0.5, 1.0]
    assert_array_almost_equal(actual_levels, expected_levels, decimal=10)
    
    plt.close(fig)


def test_contour_boolean_explicit_levels_still_work():
    """Test that explicit levels still work for boolean arrays."""
    # Create a boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10) > 0.5
    
    # Test contour with explicit levels - should still work
    fig, ax = plt.subplots()
    cs = ax.contour(data, levels=[0.2, 0.8])
    
    # Should use the explicit levels
    expected_levels = [0.2, 0.8]
    actual_levels = cs.levels
    
    assert list(actual_levels) == expected_levels, f"Expected levels {expected_levels}, got {list(actual_levels)}"
    
    plt.close(fig)


def test_contourf_boolean_explicit_levels_still_work():
    """Test that explicit levels still work for boolean arrays with contourf."""
    # Create a boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10) > 0.5
    
    # Test contourf with explicit levels - should still work
    fig, ax = plt.subplots()
    cs = ax.contourf(data, levels=[0.1, 0.4, 0.7])
    
    # Should use the explicit levels
    expected_levels = [0.1, 0.4, 0.7]
    actual_levels = cs.levels
    
    assert list(actual_levels) == expected_levels, f"Expected levels {expected_levels}, got {list(actual_levels)}"
    
    plt.close(fig)


def test_contour_non_boolean_still_defaults():
    """Test that non-boolean arrays still use default 8 levels."""
    # Create a non-boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10)
    
    # Test contour with non-boolean array (should still default to 8 levels)
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Should get the default 8 levels (this is what the old behavior was)
    actual_levels = cs.levels
    
    # This should work with both old and new behavior, but we're testing it anyway
    assert len(actual_levels) == 8, f"Expected 8 default levels for non-boolean contour, got {len(actual_levels)}"
    
    plt.close(fig)


def test_contourf_non_boolean_still_defaults():
    """Test that non-boolean arrays still use default 8 levels with contourf."""
    # Create a non-boolean 2D array
    np.random.seed(42)
    data = np.random.rand(10, 10)
    
    # Test contourf with non-boolean array (should still default to 8 levels)
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # Should get the default 8 levels (this is what the old behavior was)
    actual_levels = cs.levels
    
    # This should work with both old and new behavior, but we're testing it anyway
    assert len(actual_levels) == 8, f"Expected 8 default levels for non-boolean contourf, got {len(actual_levels)}"
    
    plt.close(fig)