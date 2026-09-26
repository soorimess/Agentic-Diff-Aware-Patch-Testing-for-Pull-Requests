"""
Regression test for SubFigure legend bug.

This test ensures that legends can be added to SubFigure objects,
which was broken before the fix in matplotlib/matplotlib#20859.
"""

import matplotlib.pyplot as plt
import pytest


def test_subfigure_legend():
    """Test that legends work with SubFigure objects."""
    # Create a subfigure as described in the bug report
    fig = plt.figure()
    subfig = fig.subfigures()
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # Before the fix, this would raise:
    # TypeError: Legend needs either Axes or Figure as parent
    # After the fix, this should work without exception
    legend = subfig.legend()
    
    # If we get here, the legend was created successfully
    assert legend is not None


def test_subfigure_legend_multiple_axes():
    """Test that legends work with SubFigure objects containing multiple axes."""
    # Create a subfigure with multiple subplots
    fig = plt.figure()
    subfigs = fig.subfigures(1, 2)
    ax1 = subfigs[0].subplots()
    ax2 = subfigs[1].subplots()
    
    ax1.plot([0, 1, 2], [0, 1, 2], label="line1")
    ax2.plot([0, 1, 2], [2, 1, 0], label="line2")
    
    # Legend on first subfigure should work
    legend = subfigs[0].legend()
    
    # If we get here, the legend was created successfully
    assert legend is not None