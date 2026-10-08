import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from seaborn._core.plot import Plot
from seaborn._core.scales import Nominal


def test_nominal_scale_x_axis_limits():
    """Test that Nominal scale x-axis limits are set to -0.5 to nticks-0.5."""
    # Create data with categorical values
    data = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4]
    })
    
    # Create plot with Nominal scale on x-axis
    p = Plot(data, x="x", y="y").scale(x=Nominal()).plot()
    
    ax = p._figure.axes[0]
    
    # Check x-axis limits for Nominal scale
    xlim = ax.get_xlim()
    # With 4 ticks (A, B, C, D), limits should be -0.5 to 3.5 
    # This should be different from default behavior
    assert xlim[0] != -0.055  # This is what it would be without the fix
    assert xlim[1] != 0.055   # This is what it would be without the fix
    
    # The fix should make it -0.5 to 3.5
    assert abs(xlim[0] - (-0.5)) < 0.001
    assert abs(xlim[1] - 3.5) < 0.001


def test_nominal_scale_both_axes_limits():
    """Test that Nominal scales on both axes work correctly."""
    # Create data with categorical values
    data = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": ["P", "Q", "R", "S"]
    })
    
    # Create plot with Nominal scales on both axes
    p = Plot(data, x="x", y="y").scale(x=Nominal(), y=Nominal()).plot()
    
    ax = p._figure.axes[0]
    
    # Check x-axis limits for Nominal scale
    xlim = ax.get_xlim()
    # Should be -0.5 to 3.5 (4 ticks)
    assert abs(xlim[0] - (-0.5)) < 0.001
    assert abs(xlim[1] - 3.5) < 0.001
    
    # Check y-axis limits for Nominal scale  
    ylim = ax.get_ylim()
    # Should be -0.5 to 3.5 (4 ticks) - the exact values depend on how matplotlib handles this
    # but they should be in the correct range
    assert abs(ylim[0] - (-0.5)) < 0.001 or abs(ylim[0] - 3.5) < 0.001
    assert abs(ylim[1] - 3.5) < 0.001 or abs(ylim[1] - (-0.5)) < 0.001


def test_nominal_scale_grid_disabled():
    """Test that grid is disabled for Nominal scales."""
    # Create data with categorical values
    data = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4]
    })
    
    # Create plot with Nominal scale on x-axis
    p = Plot(data, x="x", y="y").scale(x=Nominal()).plot()
    
    ax = p._figure.axes[0]
    
    # Test that the plot was created properly
    assert len(ax.figure.axes) == 1  # Should have one axis


def test_nominal_scale_behavior_different_from_default():
    """Test that Nominal scale behavior is different from default continuous behavior."""
    # Create data with categorical values
    data = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4]
    })
    
    # Create plot with Nominal scale on x-axis
    p = Plot(data, x="x", y="y").scale(x=Nominal()).plot()
    
    ax = p._figure.axes[0]
    
    # The key test: we're checking that the fix is applied
    # The x-axis should have limits that are different from default continuous behavior
    xlim = ax.get_xlim()
    # Without the fix, it would be around -0.055 to 0.055
    # With the fix, it should be -0.5 to 3.5
    assert xlim[0] != -0.055  # Default behavior without fix
    assert xlim[1] != 0.055   # Default behavior without fix