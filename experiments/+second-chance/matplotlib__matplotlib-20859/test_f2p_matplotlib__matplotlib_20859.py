"""
Test for the issue where adding a legend to a SubFigure doesn't work.

This test covers the regression that would have occurred if the fix
for SubFigure legend support wasn't applied.
"""

import matplotlib.pyplot as plt
import pytest


def test_subfigure_legend():
    """
    Test that legend works on SubFigure.
    
    This reproduces the bug reported where calling subfig.legend() on a 
    SubFigure would raise TypeError: "Legend needs either Axes or Figure as parent"
    """
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes in the subfigure
    ax = subfig.subplots()
    
    # Add some data to the axes
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work without raising an error
    # Previously this would raise TypeError 
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_lines')
    # The legend should have the label from the plotted line
    # Note: The actual text content depends on implementation details


def test_subfigure_legend_multiple_handles():
    """
    Test that legend works with multiple handles on SubFigure.
    """
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes in the subfigure
    ax = subfig.subplots()  
    
    # Add multiple data series
    ax.plot([0, 1, 2], [0, 1, 2], label="line1")
    ax.plot([0, 1, 2], [2, 1, 0], label="line2")
    
    # This should work without raising an error
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_lines')


def test_figure_legend_still_works():
    """
    Test that normal Figure legend functionality still works
    (regression test that our change doesn't break existing behavior)
    """
    # Create a normal figure
    fig, ax = plt.subplots()
    
    # Add some data to the axes
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work as before
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_lines')