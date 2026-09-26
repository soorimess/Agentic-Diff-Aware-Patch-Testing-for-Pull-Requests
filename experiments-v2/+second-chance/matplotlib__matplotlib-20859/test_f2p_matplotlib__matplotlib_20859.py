"""
Test for the bug where adding a legend to a SubFigure doesn't work.

This test verifies that legends can be added to SubFigure objects,
which was broken before the fix that changed the isinstance check
from Figure to FigureBase.
"""

import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that a legend can be added to a SubFigure."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes in the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work - adding legend to subfigure
    # Before the fix, this would raise TypeError: Legend needs either Axes or Figure as parent
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legends still work on regular Figure objects."""
    # Create a regular figure
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    
    plt.close(fig)


def test_legend_on_axes_still_works():
    """Test that legends still work on Axes objects."""
    # Create a figure with axes
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = ax.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    
    plt.close(fig)


def test_subfigure_is_figurebase():
    """Test that SubFigure is indeed a FigureBase."""
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Verify that SubFigure is an instance of FigureBase
    from matplotlib.figure import FigureBase
    assert isinstance(subfig, FigureBase)
    
    plt.close(fig)