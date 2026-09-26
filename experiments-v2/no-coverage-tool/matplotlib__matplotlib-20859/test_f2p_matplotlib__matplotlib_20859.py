"""
Regression test for matplotlib issue #20859:
Adding a legend to a SubFigure doesn't work
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that legend works on SubFigure - this should pass after the fix."""
    # This reproduces the exact code from the bug report
    subfig = plt.figure().subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work but currently raises TypeError
    # The test will fail on the old code and pass on the fixed code
    legend = subfig.legend()
    
    # If we get here without exception, the test passes
    assert legend is not None


def test_legend_on_figure_still_works():
    """Test that legend still works on regular Figure."""
    # This should continue to work
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    legend = fig.legend()
    
    # Verify the legend was created successfully
    assert legend is not None


if __name__ == "__main__":
    test_legend_on_subfigure()
    test_legend_on_figure_still_works()
    print("All tests passed!")