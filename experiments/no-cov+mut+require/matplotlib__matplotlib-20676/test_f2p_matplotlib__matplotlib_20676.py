"""
Regression test for SpanSelector interactive mode forcing axes limits to include 0.

This test ensures that when a SpanSelector is created with interactive=True,
the axis limits are not unnecessarily expanded to include 0, which was a 
regression from matplotlib 3.4 behavior.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_span_selector_interactive_no_force_zero_xlimits():
    """
    Test that interactive SpanSelector does not force x-axis limits to include 0.
    
    When creating a SpanSelector with interactive=True on data that doesn't
    include 0, the x-axis limits should remain unchanged, not be expanded
    to include 0.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create SpanSelector with interactive=True (the problematic case)
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should NOT have changed (no forced inclusion of 0)
    # The bug was that limits were expanded to include 0
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when they should remain unchanged"
    )
    
    plt.close(fig)


def test_span_selector_interactive_no_force_zero_ylimits():
    """
    Test that interactive SpanSelector does not force y-axis limits to include 0.
    
    When creating a SpanSelector with interactive=True on data that doesn't
    include 0, the y-axis limits should remain unchanged, not be expanded
    to include 0.
    """
    # Create figure and axis with data that doesn't include 0  
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create SpanSelector with interactive=True
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The y-limits should NOT have changed (no forced inclusion of 0)
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} "
        "when they should remain unchanged"
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_unchanged():
    """
    Test that non-interactive SpanSelector behavior is unchanged.
    
    This ensures we're only testing the interactive change.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create SpanSelector with interactive=False (should be unchanged)
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain unchanged
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when they should remain unchanged"
    )
    
    plt.close(fig)


def test_span_selector_interactive_0_in_data_still_works():
    """
    Test that when data legitimately includes 0, it should still be included.
    """
    # Create figure and axis with data that includes 0
    fig, ax = plt.subplots()
    ax.plot([-10, 10], [10, 20])
    
    # Get initial x-limits  
    initial_xlim = ax.get_xlim()
    
    # Create SpanSelector with interactive=True
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # Limits should not change
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when they should remain unchanged"
    )
    
    plt.close(fig)


if __name__ == "__main__":
    test_span_selector_interactive_no_force_zero_xlimits()
    test_span_selector_interactive_no_force_zero_ylimits()
    test_span_selector_non_interactive_unchanged()
    test_span_selector_interactive_0_in_data_still_works()
    print("All tests passed!")