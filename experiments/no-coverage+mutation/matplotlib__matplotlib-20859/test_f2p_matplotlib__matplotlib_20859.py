"""
Test for the specific bug where adding a legend to a SubFigure doesn't work.

This test ensures that calling legend() on a SubFigure works correctly,
which was broken before the fix that changed the isinstance check from
Figure to FigureBase in legend.py.
"""

import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend() can be called on a SubFigure object."""
    # Create a main figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes in the subfigure
    ax = subfig.subplots()
    
    # Add data with labels
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work after the fix, but fail before the fix
    # The bug was that isinstance(subfig, Figure) is False but isinstance(subfig, FigureBase) is True
    legend = subfig.legend()
    
    # Verify the legend was created correctly
    assert legend is not None
    assert len(legend.get_lines()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


def test_legend_on_figure_still_works():
    """Test that legend() still works on regular Figure objects."""
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    legend = fig.legend()
    
    # Verify the legend was created correctly
    assert legend is not None
    assert len(legend.get_lines()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close(fig)


if __name__ == "__main__":
    test_legend_on_subfigure()
    test_legend_on_figure_still_works()
    print("All tests passed!")