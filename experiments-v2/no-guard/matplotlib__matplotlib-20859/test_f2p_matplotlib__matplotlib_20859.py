"""
Test for matplotlib issue #20859: Adding a legend to a SubFigure doesn't work.

This test ensures that legends can be added to SubFigure objects, which
should work since SubFigure is a subclass of FigureBase.
"""
import matplotlib.pyplot as plt


def test_legend_on_subfigure():
    """Test that a legend can be added to a SubFigure."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work - adding legend to subfigure
    # Before the fix, this would raise TypeError: "Legend needs either Axes or Figure as parent"
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert legend.get_title().get_text() == ""
    
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legends still work on regular Figure objects."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    
    plt.close(fig)


def test_legend_on_axes_still_works():
    """Test that legends still work on Axes objects."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = ax.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    
    plt.close(fig)