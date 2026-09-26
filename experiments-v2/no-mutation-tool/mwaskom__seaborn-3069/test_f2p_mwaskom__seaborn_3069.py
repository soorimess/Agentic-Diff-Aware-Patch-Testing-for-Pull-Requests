import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from seaborn._core.plot import Plot
from seaborn._core.scales import Nominal


def test_nominal_scale_axis_limits():
    """Test that Nominal scales use -0.5 to nticks-0.5 limits."""
    # Create data with categorical values
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D'],
        'y': [1, 2, 3, 4]
    })
    
    # Create a plot with Nominal scale on x-axis
    p = Plot(data, x='x', y='y').scale(x=Nominal())
    
    # Generate the plot and get the plotter
    plotter = p.plot()
    
    # Access the axes from the plotter - check the structure
    # The subplots is an iterable, so we can iterate over it
    for sub in plotter._subplots:
        ax = sub["ax"]
        # Get the x-axis limits
        xlim = ax.get_xlim()
        
        # For Nominal scale with 4 categories, limits should be -0.5 to 3.5
        # Before fix: would use normal margin logic (probably something like -0.5 to 4.5 or similar)
        # After fix: should be exactly -0.5 to 3.5
        assert xlim[0] == -0.5
        assert xlim[1] == 3.5
        break  # Only test first subplot


def test_nominal_scale_y_axis_inversion():
    """Test that y-axis Nominal scales are inverted."""
    # Create data with categorical values
    data = pd.DataFrame({
        'x': [1, 2, 3, 4],
        'y': ['A', 'B', 'C', 'D']
    })
    
    # Create a plot with Nominal scale on y-axis
    p = Plot(data, x='x', y='y').scale(y=Nominal())
    
    # Generate the plot and get the plotter
    plotter = p.plot()
    
    # Access the axes from the plotter
    for sub in plotter._subplots:
        ax = sub["ax"]
        # Get the y-axis limits
        ylim = ax.get_ylim()
        
        # For y-axis Nominal scale with 4 categories, limits should be inverted
        # Before fix: would use normal margin logic (probably 0.5 to 4.5 or similar)
        # After fix: should be 3.5 to -0.5 (inverted)
        assert ylim[0] == 3.5  # high value first
        assert ylim[1] == -0.5  # low value second
        break  # Only test first subplot


def test_nominal_scale_with_explicit_limits():
    """Test that Nominal scales respect explicit limits."""
    # Create data with categorical values
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D'],
        'y': [1, 2, 3, 4]
    })
    
    # Create a plot with Nominal scale and explicit limits
    p = Plot(data, x='x', y='y').scale(x=Nominal()).limit(x=(0, 2))
    
    # Generate the plot and get the plotter
    plotter = p.plot()
    
    # Access the axes from the plotter
    for sub in plotter._subplots:
        ax = sub["ax"]
        # With explicit limits, normal behavior should be used
        # This tests that the special Nominal behavior is only applied when no limits are set
        xlim = ax.get_xlim()
        
        # Should respect explicit limits, not use Nominal-specific limits
        assert xlim[0] == 0
        assert xlim[1] == 2
        break  # Only test first subplot