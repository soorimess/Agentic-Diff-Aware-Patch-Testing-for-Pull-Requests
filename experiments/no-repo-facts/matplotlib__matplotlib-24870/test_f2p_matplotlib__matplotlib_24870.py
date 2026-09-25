"""
Test for bug fix related to auto-detecting bool arrays in contour().

This test checks that when a boolean 2D array is passed to contour() or contourf()
without specifying levels, it defaults to appropriate levels for boolean data:
- contour(boolean_array) should default to levels=[.5] 
- contourf(boolean_array) should default to levels=[0, .5, 1]
"""

import numpy as np
import matplotlib.pyplot as plt


def test_contour_bool_auto_levels():
    """Test that contour() with boolean array auto-selects levels=[.5]"""
    # Create a test boolean array (4x4 just to be definite)
    z = np.array([[True, False, True, False],
                  [False, True, False, True],
                  [True, False, True, False], 
                  [False, True, False, True]])
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Call contour with boolean array (no levels specified)
    cs = ax.contour(z)
    
    # The contour should have levels=[.5] by default (changed behavior)
    expected_levels = [.5]  
    assert list(cs.levels) == expected_levels, f"Expected levels {expected_levels}, got {list(cs.levels)}"
    
    plt.close(fig)


def test_contourf_bool_auto_levels():
    """Test that contourf() with boolean array auto-selects levels=[0, .5, 1]"""
    # Create a test boolean array
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Call contourf with boolean array (no levels specified)
    cs = ax.contourf(z)
    
    # The contourf should have levels=[0, .5, 1] by default (changed behavior)
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels, f"Expected levels {expected_levels}, got {list(cs.levels)}"
    
    plt.close(fig)


def test_contour_bool_vs_regular_behavior():
    """Test that boolean and regular arrays have different default behaviors"""
    # Create boolean and float arrays of the same shape
    bool_z = np.array([[True, False, True],
                       [False, True, False],
                       [True, False, True]])
    
    float_z = np.array([[0.1, 0.4, 0.7],
                        [0.2, 0.5, 0.8], 
                        [0.3, 0.6, 0.9]])
    
    # Test contour behavior (boolean v regular)
    fig, ax = plt.subplots()
    cs_bool = ax.contour(bool_z)
    cs_float = ax.contour(float_z)
    
    # Boolean should get [0.5], float should get many levels
    assert list(cs_bool.levels) == [.5], f"Boolean case should get [.5], got {list(cs_bool.levels)}"
    assert len(cs_float.levels) > 1, f"Float case should get multiple levels, got {len(cs_float.levels)}"
    
    plt.close(fig)
    
    # Test contourf behavior (boolean v regular)  
    fig, ax = plt.subplots()
    cs_bool_f = ax.contourf(bool_z)
    cs_float_f = ax.contourf(float_z)
    
    # Boolean should get [0, 0.5, 1], float should get many levels
    assert list(cs_bool_f.levels) == [0, 0.5, 1], f"Boolean contourf should get [0, 0.5, 1], got {list(cs_bool_f.levels)}"
    assert len(cs_float_f.levels) > 1, f"Float contourf case should get multiple levels, got {len(cs_float_f.levels)}"
    
    plt.close(fig)


def test_contour_without_args_still_works():
    """Test that existing contour behavior is preserved for non-boolean arrays"""
    # Test that contour with a regular array still works (undeclared behavior, just making sure nothing broke)
    z = np.array([[0.1, 0.4, 0.7],
                  [0.2, 0.5, 0.8],
                  [0.3, 0.6, 0.9]])
    
    fig, ax = plt.subplots()
    cs = ax.contour(z)
    
    # Just ensure it returns a contour set - don't check on specific values
    assert hasattr(cs, 'levels'), "Should create a contour set with levels"
    
    plt.close(fig)


def test_contourf_without_args_still_works():
    """Test that existing contourf behavior is preserved for non-boolean arrays"""
    # Test that contourf with a regular array still works 
    z = np.array([[0.1, 0.4, 0.7],
                  [0.2, 0.5, 0.8],
                  [0.3, 0.6, 0.9]])
    
    fig, ax = plt.subplots()
    cs = ax.contourf(z)
    
    # Just ensure it returns a contour set - don't check on specific values  
    assert hasattr(cs, 'levels'), "Should create a contour set with levels"
    
    plt.close(fig)


if __name__ == "__main__":
    test_contour_bool_auto_levels()
    test_contourf_bool_auto_levels()
    test_contour_bool_vs_regular_behavior()
    test_contour_without_args_still_works()
    test_contourf_without_args_still_works()
    print("All tests passed!")