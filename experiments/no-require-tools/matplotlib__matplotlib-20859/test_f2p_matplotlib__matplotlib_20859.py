"""
Test to reproduce and verify the fix for SubFigure.legend() bug.

This test ensures that adding a legend to a SubFigure works correctly,
which was broken before the fix that changed isinstance(parent, Figure)
to isinstance(parent, FigureBase) in legend.py.
"""

import matplotlib.pyplot as plt
import pytest


def test_subfigure_legend():
    """Test that SubFigure.legend() works correctly."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Add an axes to the subfigure
    ax = subfig.subplots()
    
    # Plot something with a label
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work (was raising TypeError before the fix)
    legend = subfig.legend()
    
    # Verify the legend was created correctly
    assert legend is not None
    assert hasattr(legend, 'get_lines')
    assert len(legend.get_children()) > 0


def test_subfigure_legend_with_explicit_handles_labels():
    """Test that SubFigure.legend() works with explicit handles and labels."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Add an axes to the subfigure
    ax = subfig.subplots()
    
    # Plot something
    line, = ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work with explicit handles and labels
    legend = subfig.legend(handles=[line], labels=["test"])
    
    # Verify the legend was created correctly
    assert legend is not None
    assert hasattr(legend, 'get_lines')


if __name__ == "__main__":
    test_subfigure_legend()
    test_subfigure_legend_with_explicit_handles_labels()
    print("All tests passed!")