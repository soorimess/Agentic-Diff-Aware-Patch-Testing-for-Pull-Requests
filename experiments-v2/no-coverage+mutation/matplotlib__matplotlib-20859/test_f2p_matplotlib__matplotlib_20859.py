"""
Regression test for matplotlib issue #20859:
Adding a legend to a SubFigure doesn't work
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend() works on SubFigure objects."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()  # This returns a single SubFigure
    
    # Create an axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an error
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


def test_legend_on_subfigure_multiple_plots():
    """Test that legend() works on SubFigure objects with multiple plots."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()  # This returns a single SubFigure
    
    # Create axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="line1")
    ax.plot([0, 1, 2], [2, 1, 0], label="line2")
    
    # This should not raise an error
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 2
    
    plt.close(fig)