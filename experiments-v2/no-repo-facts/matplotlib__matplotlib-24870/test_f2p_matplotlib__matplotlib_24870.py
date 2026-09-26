"""
Test for matplotlib bug fix: Auto-detect bool arrays passed to contour()
This test verifies that boolean arrays passed to contour() automatically
get levels set to [0.5] instead of the default 7 levels.
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.testing import assert_array_equal


def test_contour_boolean_array_default_levels():
    """Test that boolean arrays get default level [0.5] instead of 7 levels."""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour (not filled) with just z array - simple case
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array)
    
    # Before fix: would use 7 default levels [0., 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05]
    # After fix: should use [0.5] for boolean arrays
    expected_levels = np.array([0.5])
    
    # Use assert_array_equal to avoid the "ambiguous truth value" issue
    assert_array_equal(cs.levels, expected_levels, 
                      err_msg=f"Expected levels {expected_levels}, got {cs.levels}")
    
    plt.close(fig)


def test_contourf_boolean_array_default_levels():
    """Test that boolean arrays get default levels [0, 0.5, 1] for contourf."""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contourf (filled)
    fig, ax = plt.subplots()
    cs = ax.contourf(bool_array)
    
    # Before fix: would use 7 default levels [0., 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05]
    # After fix: should use [0, 0.5, 1] for boolean arrays in contourf
    expected_levels = np.array([0, 0.5, 1])
    
    # Use assert_array_equal to avoid the "ambiguous truth value" issue
    assert_array_equal(cs.levels, expected_levels, 
                      err_msg=f"Expected levels {expected_levels}, got {cs.levels}")
    
    plt.close(fig)


def test_contour_boolean_array_with_xy_arrays():
    """Test that boolean arrays work with explicit x,y,z arrays."""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Create coordinate arrays
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    
    # Test contour with x, y, z arrays - this hits the nargs > 2 path
    fig, ax = plt.subplots()
    cs = ax.contour(x, y, bool_array)
    
    # Should still use [0.5] for boolean arrays even with explicit x,y,z
    expected_levels = np.array([0.5])
    assert_array_equal(cs.levels, expected_levels, 
                      err_msg=f"Expected levels {expected_levels}, got {cs.levels}")
    
    plt.close(fig)


def test_contourf_boolean_array_with_xy_arrays():
    """Test that boolean arrays work with explicit x,y,z arrays for contourf."""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Create coordinate arrays
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    
    # Test contourf with x, y, z arrays - this hits the nargs > 2 path
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, bool_array)
    
    # Should still use [0, 0.5, 1] for boolean arrays even with explicit x,y,z
    expected_levels = np.array([0, 0.5, 1])
    assert_array_equal(cs.levels, expected_levels, 
                      err_msg=f"Expected levels {expected_levels}, got {cs.levels}")
    
    plt.close(fig)


def test_contour_non_boolean_array_still_works():
    """Test that non-boolean arrays still work as before."""
    # Create a regular float 2D array with values that don't include 0.5
    float_array = np.array([[0.1, 0.2, 0.3],
                           [0.4, 0.6, 0.7],
                           [0.8, 0.9, 1.0]])
    
    # Test contour with regular array (should still use default 7 levels)
    fig, ax = plt.subplots()
    cs = ax.contour(float_array)
    
    # Should use default 7 levels for non-boolean arrays (not [0.5])
    # The important thing is that it should NOT be [0.5] 
    assert len(cs.levels) > 1, f"Expected multiple levels, got {cs.levels}"
    assert not np.array_equal(cs.levels, [0.5]), f"Non-boolean arrays should not default to [0.5] levels, got {cs.levels}"
    
    plt.close(fig)


def test_contour_explicit_levels_override():
    """Test that explicit levels still override the automatic behavior."""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array, levels=[0.2, 0.8])
    
    # Should use the explicitly provided levels, not the automatic [0.5]
    expected_levels = np.array([0.2, 0.8])
    assert_array_equal(cs.levels, expected_levels, 
                      err_msg=f"Expected explicit levels {expected_levels}, got {cs.levels}")
    
    plt.close(fig)


if __name__ == "__main__":
    # Run the tests
    test_contour_boolean_array_default_levels()
    test_contourf_boolean_array_default_levels()
    test_contour_boolean_array_with_xy_arrays()
    test_contourf_boolean_array_with_xy_arrays()
    test_contour_non_boolean_array_still_works()
    test_contour_explicit_levels_override()
    print("All tests passed!")