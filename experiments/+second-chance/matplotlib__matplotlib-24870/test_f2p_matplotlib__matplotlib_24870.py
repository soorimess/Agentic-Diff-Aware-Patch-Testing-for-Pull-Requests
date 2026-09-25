"""
Test for boolean array auto-detection in contour().

This regression test ensures that boolean 2D arrays automatically
default to appropriate contour levels (0.5 for contour, [0, 0.5, 1] for contourf).
"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import pytest


def test_contour_boolean_auto_levels():
    """
    Test that boolean arrays in contour() default to level [0.5].
    """
    # Create a boolean 2D array
    bool_array = np.array([[True, False], [False, True]])
    
    # Set up the plot without explicit levels
    fig, ax = plt.subplots()
    contour_obj = ax.contour(bool_array)
    
    # Check that the levels are [0.5] for contour (non-filled)
    expected_levels = [0.5]
    
    # We access the internal levels through the contour object's levels attribute
    np.testing.assert_array_equal(contour_obj.levels, expected_levels)
    
    plt.close(fig)


def test_contourf_boolean_auto_levels():
    """
    Test that boolean arrays in contourf() default to levels [0, 0.5, 1].
    """
    # Create a boolean 2D array
    bool_array = np.array([[True, False], [False, True]])
    
    # Set up the plot without explicit levels
    fig, ax = plt.subplots()
    contourf_obj = ax.contourf(bool_array)
    
    # Check that the levels are [0, 0.5, 1] for contourf (filled)
    expected_levels = [0, 0.5, 1]
    
    # We access the internal levels through the contour object's levels attribute
    np.testing.assert_array_equal(contourf_obj.levels, expected_levels)
    
    plt.close(fig)


def test_contour_boolean_with_explicit_levels_untouched():
    """
    Test that explicit levels are still respected even for boolean arrays.
    """
    # Create a boolean 2D array
    bool_array = np.array([[True, False], [False, True]])
    
    # Set up the plot with explicit levels
    fig, ax = plt.subplots()
    contour_obj = ax.contour(bool_array, levels=[0.25, 0.75])
    
    # Should use the explicitly provided levels
    expected_levels = [0.25, 0.75]
    np.testing.assert_array_equal(contour_obj.levels, expected_levels)
    
    plt.close(fig)


def test_contour_regular_float_still_uses_default():
    """
    Test that regular float arrays still use the default behavior.
    """
    # Create a regular float array (not boolean)
    float_array = np.array([[0.1, 0.2], [0.8, 0.9]])
    
    # Set up the plot without explicit levels
    fig, ax = plt.subplots()
    contour_obj = ax.contour(float_array)
    
    # Should get 7 levels by default (this varies based on data range, but the number should be significant)
    # But more precisely, we know that the default behavior with the right data should work
    assert len(contour_obj.levels) >= 3  # Should be more than a few
    
    # The default must be using autolev(), which auto-generates levels
    plt.close(fig)


def test_contourf_regular_float_still_uses_default():
    """
    Test that regular float arrays still use the default contourf behavior.
    """
    # Create a regular float array (not boolean)
    float_array = np.array([[0.1, 0.2], [0.8, 0.9]])
    
    # Set up the plot without explicit levels
    fig, ax = plt.subplots()
    contourf_obj = ax.contourf(float_array)
    
    # Should get 7 levels by default
    assert len(contourf_obj.levels) >= 3
    
    plt.close(fig)


# Make sure that the boolean array detection doesn't affect argument processing
def test_contour_with_3d_inputs():
    """
    Test that contour still works with 3D input arrays (x,y,z), which should 
    also trigger boolean detection when appropriate.
    """
    # Create coordinates and a boolean array
    x = np.array([0, 1])
    y = np.array([0, 1])
    bool_array = np.array([[True, False], [False, True]])
    
    # Set up the plot with 3D input
    fig, ax = plt.subplots()
    contour_obj = ax.contour(x, y, bool_array)
    
    # Should still default to [0.5] levels for boolean input
    expected_levels = [0.5]
    np.testing.assert_array_equal(contour_obj.levels, expected_levels)
    
    plt.close(fig)


# Make sure that boolean dtype detection works properly
def test_ensure_boolean_dtype_recognition():
    """
    Test that boolean dtype is properly detected in the non-filled case.
    """
    bool_array = np.array([[True, False], [False, True]], dtype=bool)
    fig, ax = plt.subplots()
    contour_obj = ax.contour(bool_array)
    
    # This would test the data-path specifically 
    expected_levels = [0.5]
    np.testing.assert_array_equal(contour_obj.levels, expected_levels)
    
    plt.close(fig)