"""
Test for matplotlib issue #20859: Adding a legend to a SubFigure doesn't work

This test verifies that legends can be added to SubFigure objects,
which was broken before the fix.
"""

import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend() works on SubFigure objects."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work (before the fix it would raise TypeError)
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legend() still works on regular Figure objects."""
    # Create a regular figure
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    plt.close(fig)


def test_legend_on_axes_still_works():
    """Test that legend() still works on Axes objects."""
    # Create a figure with axes
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = ax.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    plt.close(fig)