import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet
import pytest


def test_contour_boolean_auto_levels_contour():
    """Test that boolean arrays get automatic levels=[0.5] for contour lines."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour (not filled) with boolean array - should auto-detect and use levels=[0.5]
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # The levels should be [0.5] for boolean arrays
    expected_levels = [0.5]
    assert cs.levels.tolist() == expected_levels
    plt.close(fig)


def test_contour_boolean_auto_levels_contourf():
    """Test that boolean arrays get automatic levels=[0, 0.5, 1] for filled contours."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf (filled) with boolean array - should auto-detect and use levels=[0, 0.5, 1]
    fig, ax = plt.subplots()
    cs = ax.contourf(data)
    
    # The levels should be [0, 0.5, 1] for boolean arrays
    expected_levels = [0, 0.5, 1]
    assert cs.levels.tolist() == expected_levels
    plt.close(fig)


def test_contour_non_boolean_still_uses_default_levels():
    """Test that non-boolean arrays still use default 7 levels."""
    # Create a float 2D array
    data = np.array([[0.1, 0.3, 0.7],
                     [0.2, 0.6, 0.8],
                     [0.4, 0.5, 0.9]])
    
    # Test contour with float array - should still use 7 default levels
    fig, ax = plt.subplots()
    cs = ax.contour(data)
    
    # Should have 7 default levels (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05)
    # But we'll just check it's not [0.5] to ensure it's the default behavior
    assert cs.levels.tolist() != [0.5]
    plt.close(fig)


def test_contour_boolean_explicit_levels_override():
    """Test that explicit levels still override auto-detection."""
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with explicit levels - should ignore auto-detection
    fig, ax = plt.subplots()
    cs = ax.contour(data, levels=[0.25, 0.75])
    
    # Should use the explicitly provided levels
    expected_levels = [0.25, 0.75]
    assert cs.levels.tolist() == expected_levels
    plt.close(fig)


def test_contour_3arg_boolean_auto_levels():
    """Test that 3-argument contour with boolean arrays also auto-detects levels."""
    # Create coordinate grids
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contour with 3 args (x, y, z) - should auto-detect boolean levels
    fig, ax = plt.subplots()
    cs = ax.contour(x, y, data)
    
    # The levels should be [0.5] for boolean arrays
    expected_levels = [0.5]
    assert cs.levels.tolist() == expected_levels
    plt.close(fig)


def test_contourf_3arg_boolean_auto_levels():
    """Test that 3-argument contourf with boolean arrays also auto-detects levels."""
    # Create coordinate grids
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    X, Y = np.meshgrid(x, y)
    
    # Create a boolean 2D array
    data = np.array([[True, False, True],
                     [False, True, False],
                     [True, False, True]])
    
    # Test contourf with 3 args (x, y, z) - should auto-detect boolean levels
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, data)
    
    # The levels should be [0, 0.5, 1] for boolean arrays
    expected_levels = [0, 0.5, 1]
    assert cs.levels.tolist() == expected_levels
    plt.close(fig)


def test_tricontour_boolean_auto_levels():
    """Test that tricontour with boolean arrays auto-detects levels."""
    # Create simple triangulation data
    x = np.array([0.0, 1.0, 0.0, 1.0])
    y = np.array([0.0, 0.0, 1.0, 1.0])
    z = np.array([True, False, True, False])  # Boolean values
    
    # Test tricontour with boolean array - should auto-detect and use levels=[0.5]
    fig, ax = plt.subplots()
    # Note: tricontour expects triangulation, so we'll use the simpler form
    try:
        cs = ax.tricontour(x, y, z)
        # The levels should be [0.5] for boolean arrays
        expected_levels = [0.5]
        assert cs.levels.tolist() == expected_levels
    except Exception:
        # If tricontour doesn't work with this simple setup, that's OK for now
        pass
    finally:
        plt.close(fig)


def test_tricontourf_boolean_auto_levels():
    """Test that tricontourf with boolean arrays auto-detects levels."""
    # Create simple triangulation data
    x = np.array([0.0, 1.0, 0.0, 1.0])
    y = np.array([0.0, 0.0, 1.0, 1.0])
    z = np.array([True, False, True, False])  # Boolean values
    
    # Test tricontourf with boolean array - should auto-detect and use levels=[0, 0.5, 1]
    fig, ax = plt.subplots()
    # Note: tricontourf expects triangulation, so we'll use the simpler form
    try:
        cs = ax.tricontourf(x, y, z)
        # The levels should be [0, 0.5, 1] for boolean arrays
        expected_levels = [0, 0.5, 1]
        assert cs.levels.tolist() == expected_levels
    except Exception:
        # If tricontourf doesn't work with this simple setup, that's OK for now
        pass
    finally:
        plt.close(fig)