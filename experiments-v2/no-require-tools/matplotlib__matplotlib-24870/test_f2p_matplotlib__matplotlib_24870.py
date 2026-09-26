"""
Test for auto-detection of boolean arrays in contour().

This test ensures that when boolean 2D arrays are passed to contour() 
without explicit levels, they automatically default to appropriate levels:
- [0.5] for contour (line) plots
- [0, 0.5, 1] for contourf (filled) plots
"""
import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet


def test_contour_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and use appropriate default levels."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour (line) with boolean data
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    # The default levels should be [0.5] for boolean data
    expected_levels = [0.5]
    assert list(cs.levels) == expected_levels
    plt.close(fig)
    

def test_contourf_boolean_auto_levels():
    """Test that boolean arrays get auto-detected and use appropriate default levels for filled contours."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf (filled) with boolean data
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    # The default levels should be [0, 0.5, 1] for boolean data
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contour_non_boolean_default_levels():
    """Test that non-boolean arrays still default to appropriate levels."""
    # Create a regular float 2D array
    data = np.array([[1.0, 2.0, 3.0],
                     [2.0, 3.0, 4.0],
                     [3.0, 4.0, 5.0]])
    
    # Test contour with non-boolean data
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    # Should default to 9 levels (this is current behavior)
    assert len(cs.levels) == 9
    # The exact values depend on the data range, but should be reasonable
    assert cs.levels[0] <= cs.levels[-1]
    plt.close(fig)


def test_contour_boolean_with_explicit_levels_unchanged():
    """Test that explicit levels are still respected even for boolean data."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(data, levels=[0.25, 0.75])
    # Should use the explicit levels
    expected_levels = [0.25, 0.75]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contourf_boolean_with_explicit_levels_unchanged():
    """Test that explicit levels are still respected even for boolean data with filled contours."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contourf(data, levels=[0.1, 0.3, 0.7, 0.9])
    # Should use the explicit levels
    expected_levels = [0.1, 0.3, 0.7, 0.9]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contour_3args_boolean_auto_levels():
    """Test that boolean arrays with 3-argument contour() get auto-detected."""
    # Create coordinate arrays
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 2, 3)
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour (line) with 3-argument call
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, data)
    # The default levels should be [0.5] for boolean data
    expected_levels = [0.5]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contourf_3args_boolean_auto_levels():
    """Test that boolean arrays with 3-argument contourf() get auto-detected."""
    # Create coordinate arrays
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 2, 3)
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf (filled) with 3-argument call
    fig, ax = plt.subplots()
    cs = ax.contourf(X, Y, data)
    # The default levels should be [0, 0.5, 1] for boolean data
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels
    plt.close(fig)