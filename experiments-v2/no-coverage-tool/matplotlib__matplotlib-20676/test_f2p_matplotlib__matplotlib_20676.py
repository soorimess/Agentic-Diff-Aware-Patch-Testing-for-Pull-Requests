"""
Regression test for SpanSelector interactive mode incorrectly forcing axes limits to include 0.

This test ensures that when creating a SpanSelector with interactive=True, the axes
limits are not incorrectly modified to include 0.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import pytest


def test_span_selector_interactive_axes_limits_not_modified():
    """
    Test that SpanSelector with interactive=True does not modify axis limits to include 0.
    
    This is a regression test for the bug where interactive SpanSelector would
    incorrectly force axes limits to include 0, even when the data doesn't require it.
    """
    # Create a figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get the original axis limits
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()
    
    # Create a SpanSelector with interactive=True (the problematic case)
    ss = widgets.SpanSelector(ax, print, "horizontal", interactive=True)
    
    # Check that the axis limits have not been modified
    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()
    
    # The limits should remain unchanged
    assert original_xlim == new_xlim, f"X-axis limits changed from {original_xlim} to {new_xlim}"
    assert original_ylim == new_ylim, f"Y-axis limits changed from {original_ylim} to {new_ylim}"
    
    plt.close(fig)


def test_span_selector_interactive_vertical_axes_limits_not_modified():
    """
    Test that SpanSelector with interactive=True and vertical direction does not 
    modify axis limits to include 0.
    """
    # Create a figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get the original axis limits
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()
    
    # Create a SpanSelector with interactive=True and vertical direction
    ss = widgets.SpanSelector(ax, print, "vertical", interactive=True)
    
    # Check that the axis limits have not been modified
    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()
    
    # The limits should remain unchanged
    assert original_xlim == new_xlim, f"X-axis limits changed from {original_xlim} to {new_xlim}"
    assert original_ylim == new_ylim, f"Y-axis limits changed from {original_ylim} to {new_ylim}"
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits():
    """
    Test that SpanSelector with interactive=False does not modify axis limits.
    
    This is to ensure that the non-interactive case works as expected.
    """
    # Create a figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get the original axis limits
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()
    
    # Create a SpanSelector with interactive=False
    ss = widgets.SpanSelector(ax, print, "horizontal", interactive=False)
    
    # Check that the axis limits have not been modified
    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()
    
    # The limits should remain unchanged
    assert original_xlim == new_xlim, f"X-axis limits changed from {original_xlim} to {new_xlim}"
    assert original_ylim == new_ylim, f"Y-axis limits changed from {original_ylim} to {new_ylim}"
    
    plt.close(fig)


if __name__ == "__main__":
    test_span_selector_interactive_axes_limits_not_modified()
    test_span_selector_interactive_vertical_axes_limits_not_modified()
    test_span_selector_non_interactive_axes_limits()
    print("All tests passed!")