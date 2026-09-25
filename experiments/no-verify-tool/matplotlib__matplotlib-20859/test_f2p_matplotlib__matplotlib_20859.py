"""
Test for the SubFigure legend issue.

This test ensures that adding a legend to a SubFigure works properly.
Before the fix, this would raise a TypeError because SubFigure
objects were not recognized as valid parents for legends.
"""

import matplotlib.pyplot as plt
import pytest


def test_subfigure_legend():
    """Test that legend works with SubFigure."""
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create axes in the subfigure
    ax = subfig.subplots()
    
    # Plot some data with labels
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an exception after the fix
    # Before the fix, this would raise:
    # TypeError: Legend needs either Axes or Figure as parent
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    

def test_subfigure_legend_with_multiple_axes():
    """Test that legend works with SubFigure containing multiple axes."""
    # Create a figure and subfigures
    fig = plt.figure()
    
    # For 2x1 subfigures
    subfigs = fig.subfigures(nrows=1, ncols=2)
    
    # Create axes in the subfigure  
    ax1 = subfigs[0].subplots()
    ax2 = subfigs[1].subplots()
    
    # Plot some data with labels
    ax1.plot([0, 1, 2], [0, 1, 2], label="test1")
    ax2.plot([0, 1, 2], [2, 1, 0], label="test2")
    
    # This should not raise an exception after the fix
    legend = subfigs[0].legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert hasattr(legend, 'get_texts')


if __name__ == "__main__":
    test_subfigure_legend()
    test_subfigure_legend_with_multiple_axes()
    print("All tests passed!")