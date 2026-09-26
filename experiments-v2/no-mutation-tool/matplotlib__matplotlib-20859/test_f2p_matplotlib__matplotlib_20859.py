"""
Regression test for matplotlib issue #20859.

Adding a legend to a SubFigure doesn't work.
"""
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.axes import Axes
from matplotlib.figure import Figure, FigureBase


def test_legend_on_subfigure():
    """Test that a legend can be added to a SubFigure."""
    # This should work but currently raises TypeError
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an exception
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close('all')


def test_legend_on_figure_still_works():
    """Test that a legend can still be added to a regular Figure."""
    # This should continue to work as before
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an exception
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close('all')


def test_legend_constructor_with_different_parents():
    """Test Legend constructor directly with different parent types."""
    # Test with regular Figure (should work)
    fig = plt.figure()
    legend = Legend(fig, [], [])
    assert legend is not None
    assert not legend.isaxes
    plt.close('all')
    
    # Test with SubFigure (should work after fix)
    subfig = plt.figure().subfigures()
    legend = Legend(subfig, [], [])
    assert legend is not None
    assert not legend.isaxes
    plt.close('all')
    
    # Test with Axes (should work)
    fig = plt.figure()
    ax = fig.subplots()
    legend = Legend(ax, [], [])
    assert legend is not None
    assert legend.isaxes
    plt.close('all')


if __name__ == "__main__":
    test_legend_on_subfigure()
    test_legend_on_figure_still_works()
    test_legend_constructor_with_different_parents()
    print("All tests passed!")