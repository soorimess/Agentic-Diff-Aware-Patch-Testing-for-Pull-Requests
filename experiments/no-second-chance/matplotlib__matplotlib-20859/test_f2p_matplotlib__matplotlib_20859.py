"""
Regression test for matplotlib bug where legend() fails on SubFigure.
Issue: Adding a legend to a SubFigure doesn't work
https://github.com/matplotlib/matplotlib/issues/20859
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend() works on SubFigure instances."""
    # Create a subfigure
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work but previously raised TypeError
    # "Legend needs either Axes or Figure as parent"
    legend = subfig.legend()
    
    # Verify it's a proper legend object
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    assert len(legend.get_texts()) == 1
    
    plt.close('all')


def test_legend_on_subfigure_with_multiple_plots():
    """Test that legend() works with multiple plots on SubFigure."""
    # Create a subfigure
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="line1")
    ax.plot([0, 1, 2], [2, 1, 0], label="line2")
    
    # This should work but previously raised TypeError
    legend = subfig.legend()
    
    # Verify it's a proper legend object with multiple entries
    assert legend is not None
    assert hasattr(legend, 'get_texts')
    assert len(legend.get_texts()) == 2
    
    plt.close('all')


if __name__ == "__main__":
    test_legend_on_subfigure()
    test_legend_on_subfigure_with_multiple_plots()
    print("All tests passed!")