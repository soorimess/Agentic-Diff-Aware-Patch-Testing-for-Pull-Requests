"""
Test for bug where adding legend to SubFigure fails
https://github.com/matplotlib/matplotlib/issues/20859
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend works on SubFigure objects."""
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create axes in the subfigure
    ax = subfig.subplots()
    
    # Plot something to have handles/labels
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work but currently fails with TypeError
    # "Legend needs either Axes or Figure as parent"
    legend = subfig.legend()
    
    # Verify that legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legend still works on regular Figure objects."""
    # Create a regular figure
    fig = plt.figure()
    
    # Create axes
    ax = fig.subplots()
    
    # Plot something to have handles/labels
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should always work
    legend = fig.legend()
    
    # Verify that legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)