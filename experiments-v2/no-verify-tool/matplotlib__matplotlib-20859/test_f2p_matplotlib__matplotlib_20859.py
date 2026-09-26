"""
Regression test for matplotlib issue #20859.

This test ensures that adding a legend to a SubFigure works correctly.
Before the fix, calling legend() on a SubFigure would raise a TypeError
because SubFigure is not recognized as a valid parent type for Legend.
"""

import matplotlib.pyplot as plt


def test_legend_on_subfigure():
    """Test that legend() works on SubFigure objects - exact reproduction from bug report."""
    # Exact reproduction from bug report
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work without raising an exception
    # Before the fix, this would raise:
    # TypeError: Legend needs either Axes or Figure as parent
    legend = subfig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close()


def test_legend_on_figure_still_works():
    """Test that legend() still works on regular Figure objects."""
    # Create a regular figure
    fig, ax = plt.subplots()
    
    # Plot something with a label
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    plt.close()


if __name__ == "__main__":
    test_legend_on_subfigure()
    test_legend_on_figure_still_works()
    print("All tests passed!")