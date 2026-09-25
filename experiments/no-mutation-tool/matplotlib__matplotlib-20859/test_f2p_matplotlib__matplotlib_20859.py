"""
Regression test for matplotlib/matplotlib#20859
Testing that SubFigure.legend() works correctly.

This test ensures that calling legend() on a SubFigure works properly,
which was broken before the fix that makes Legend accept FigureBase
instead of just Figure as a parent.
"""

import matplotlib.pyplot as plt
import pytest


def test_subfigure_legend():
    """Test that legend() works on SubFigure objects."""
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes inside the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise TypeError: "Legend needs either Axes or Figure as parent"
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


def test_subfigure_legend_with_multiple_lines():
    """Test that legend() works with multiple lines in SubFigure."""
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes inside the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="line1")
    ax.plot([0, 1, 2], [2, 1, 0], label="line2")
    
    # This should not raise TypeError: "Legend needs either Axes or Figure as parent"
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 2
    assert legend.get_texts()[0].get_text() == "line1"
    assert legend.get_texts()[1].get_text() == "line2"
    
    plt.close(fig)


def test_figure_legend_still_works():
    """Test that regular Figure.legend() still works (regression test)."""
    # Create a regular figure
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)