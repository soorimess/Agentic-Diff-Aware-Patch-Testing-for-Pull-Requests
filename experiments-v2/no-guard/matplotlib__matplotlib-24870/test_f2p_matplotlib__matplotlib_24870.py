"""
Regression test for auto-detection of boolean arrays in contour().

This test ensures that boolean arrays passed to contour() automatically
get default levels at 0.5, rather than the default 7 levels.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet
import matplotlib.tri as mtri


def test_contour_boolean_array_default_levels():
    """Test that boolean arrays get default level at 0.5"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour (not filled) - should default to [0.5]
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array)
    
    # The levels should be [0.5] for boolean arrays
    expected_levels = [0.5]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contourf_boolean_array_default_levels():
    """Test that boolean arrays get default levels at [0, 0.5, 1] for filled contours"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contourf (filled) - should default to [0, 0.5, 1]
    fig, ax = plt.subplots()
    cs = ax.contourf(bool_array)
    
    # The levels should be [0, 0.5, 1] for filled boolean arrays
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contour_boolean_array_explicit_levels():
    """Test that explicit levels still work for boolean arrays"""
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with explicit levels - should respect the explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(bool_array, levels=[0.25, 0.75])
    
    # The levels should be the explicit ones
    expected_levels = [0.25, 0.75]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contour_regular_array_default_levels():
    """Test that regular (non-boolean) arrays still get default 7 levels"""
    # Create a regular 2D array
    regular_array = np.array([[1.0, 2.0, 3.0],
                             [2.0, 3.0, 4.0],
                             [3.0, 4.0, 5.0]])
    
    # Test contour - should default to 7 levels
    fig, ax = plt.subplots()
    cs = ax.contour(regular_array)
    
    # The levels should be the default 7 levels (not [0.5])
    # We don't check exact values since they depend on data range, but we check it's not [0.5]
    assert list(cs.levels) != [0.5]
    plt.close(fig)


def test_contourf_regular_array_default_levels():
    """Test that regular (non-boolean) arrays still get default 7 levels for filled contours"""
    # Create a regular 2D array
    regular_array = np.array([[1.0, 2.0, 3.0],
                             [2.0, 3.0, 4.0],
                             [3.0, 4.0, 5.0]])
    
    # Test contourf - should default to 7 levels
    fig, ax = plt.subplots()
    cs = ax.contourf(regular_array)
    
    # The levels should be the default 7 levels (not [0, 0.5, 1])
    # We don't check exact values since they depend on data range, but we check it's not [0, 0.5, 1]
    assert list(cs.levels) != [0, 0.5, 1]
    plt.close(fig)


def test_contour_with_x_y_z_boolean_array():
    """Test contour with X, Y, Z arrays - should trigger nargs <= 4 path"""
    # Create coordinate arrays
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 3)
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with X, Y, Z arrays - should default to [0.5] for boolean
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, bool_array)
    
    # The levels should be [0.5] for boolean arrays
    expected_levels = [0.5]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contourf_with_x_y_z_boolean_array():
    """Test contourf with X, Y, Z arrays - should trigger nargs <= 4 path"""
    # Create coordinate arrays
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 3)
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contourf with X, Y, Z arrays - should default to [0, 0.5, 1] for boolean
    fig, ax = plt.subplots()
    cs = ax.contourf(X, Y, bool_array)
    
    # The levels should be [0, 0.5, 1] for filled boolean arrays
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_contour_with_x_y_z_levels_boolean_array():
    """Test contour with X, Y, Z, levels arrays - should trigger nargs <= 4 path"""
    # Create coordinate arrays
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 3)
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    bool_array = np.array([[True, False, True],
                          [False, True, False],
                          [True, False, True]])
    
    # Test contour with X, Y, Z, levels arrays - should respect explicit levels
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, bool_array, levels=[0.25, 0.75])
    
    # The levels should be the explicit ones
    expected_levels = [0.25, 0.75]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_tricontour_boolean_array_default_levels():
    """Test that tricontour with boolean arrays gets default level at 0.5"""
    # Create triangulation points
    x = np.array([0.0, 1.0, 0.0, 1.0, 0.5, 1.5])
    y = np.array([0.0, 0.0, 1.0, 1.0, 0.5, 1.5])
    z = np.array([True, False, True, False, True, False])  # boolean values
    
    # Create triangulation
    tri = mtri.Triangulation(x, y)
    
    # Test tricontour - should default to [0.5] for boolean arrays
    fig, ax = plt.subplots()
    cs = ax.tricontour(tri, z)
    
    # The levels should be [0.5] for boolean arrays
    expected_levels = [0.5]
    assert list(cs.levels) == expected_levels
    plt.close(fig)


def test_tricontourf_boolean_array_default_levels():
    """Test that tricontourf with boolean arrays gets default levels at [0, 0.5, 1]"""
    # Create triangulation points
    x = np.array([0.0, 1.0, 0.0, 1.0, 0.5, 1.5])
    y = np.array([0.0, 0.0, 1.0, 1.0, 0.5, 1.5])
    z = np.array([True, False, True, False, True, False])  # boolean values
    
    # Create triangulation
    tri = mtri.Triangulation(x, y)
    
    # Test tricontourf - should default to [0, 0.5, 1] for boolean arrays
    fig, ax = plt.subplots()
    cs = ax.tricontourf(tri, z)
    
    # The levels should be [0, 0.5, 1] for filled boolean arrays
    expected_levels = [0, 0.5, 1]
    assert list(cs.levels) == expected_levels
    plt.close(fig)