"""
Regression test for matplotlib/matplotlib#24870
Test that boolean arrays passed to contour() are auto-detected and
default to appropriate levels.
"""
import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.contour import ContourSet


def test_contour_boolean_auto_levels_filled():
    """Test that filled contours with boolean arrays default to [0, 0.5, 1]."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test filled contour
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # Should have levels [0, 0.5, 1] for boolean data
    expected_levels = [0, 0.5, 1]
    assert np.allclose(cs.levels, expected_levels)
    plt.close(fig)


def test_contour_boolean_auto_levels_line():
    """Test that line contours with boolean arrays default to [0.5]."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test line contour
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Should have levels [0.5] for boolean data
    expected_levels = [0.5]
    assert np.allclose(cs.levels, expected_levels)
    plt.close(fig)


def test_contour_boolean_with_explicit_levels():
    """Test that explicit levels still work with boolean arrays."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test with explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(data, levels=[0.25, 0.75])
    
    # Should use explicit levels
    expected_levels = [0.25, 0.75]
    assert np.allclose(cs.levels, expected_levels)
    plt.close(fig)


def test_contour_boolean_with_different_shapes():
    """Test boolean auto-detection with different array shapes."""
    # Test with larger boolean array
    data = np.random.rand(10, 10) > 0.5
    
    # Test filled contour
    fig1, ax1 = plt.subplots()
    cs_filled = ax1.contourf(data)
    expected_filled_levels = [0, 0.5, 1]
    assert np.allclose(cs_filled.levels, expected_filled_levels)
    plt.close(fig1)
    
    # Test line contour
    fig2, ax2 = plt.subplots()
    cs_line = ax2.contour(data)
    expected_line_levels = [0.5]
    assert np.allclose(cs_line.levels, expected_line_levels)
    plt.close(fig2)