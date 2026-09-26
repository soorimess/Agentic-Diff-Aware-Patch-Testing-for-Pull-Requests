"""
Regression test for matplotlib issue #20859.

Adding a legend to a SubFigure doesn't work.
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend() works on SubFigure objects."""
    # Create a subfigure
    fig = plt.figure()
    subfig = fig.subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an error
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legend() still works on regular Figure objects."""
    # Create a regular figure
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work as before
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)