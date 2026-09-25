"""
Test for bug fix related to legend on SubFigure.

This regression test ensure that adding a legend to a SubFigure works properly.
The issue was that Legend.__init__() only accepted Figure but not FigureBase,
causing a TypeError when trying to create a legend on SubFigure.
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend can be added to a SubFigure."""
    # Create figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create axes and plot data
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work without raising a TypeError
    # Before the fix, this would raise:
    # TypeError: Legend needs either Axes or Figure as parent
    legend = subfig.legend()
    
    # Verify that a legend was created
    assert legend is not None
    assert hasattr(legend, 'get_lines')
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legend still works on regular Figure (regression test)."""
    # Create regular figure
    fig = plt.figure()
    
    # Create axes and plot data
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work without raising a TypeError
    legend = fig.legend()
    
    # Verify that a legend was created
    assert legend is not None
    assert hasattr(legend, 'get_lines')
    plt.close(fig)


def test_legend_on_axes_still_works():
    """Test that legend still works on Axes (regression test)."""
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Plot data
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work without raising a TypeError
    legend = ax.legend()
    
    # Verify that a legend was created
    assert legend is not None
    assert hasattr(legend, 'get_lines')
    plt.close(fig)


def test_legend_with_direct_figure_base_parent():
    """Test that legend works with a direct FigureBase subclass (covers all code paths)."""
    # This test specifically ensures that the FigureBase isinstance check
    # is working correctly (the core fix in the PR)
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Add a few plots so objects have handles/labels
    ax1 = subfig.subplots()
    ax1.plot([0, 1], [0, 1], label="line1")
    ax2 = subfig.subplots()
    ax2.plot([0, 2], [0, 4], label="line2")
    
    # This should work now (the main scenario this PR fixed)
    legend = subfig.legend()
    
    # Verify that a legend was created
    assert legend is not None
    assert hasattr(legend, 'get_lines') 
    plt.close(fig)