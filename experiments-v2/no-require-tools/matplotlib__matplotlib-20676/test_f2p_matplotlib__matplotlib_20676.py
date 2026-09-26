"""
Regression test for SpanSelector interactive mode forcing axes limits to include 0.

This test ensures that when creating an interactive SpanSelector, the axes limits
are not incorrectly expanded to include 0.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import pytest


def test_spanselector_interactive_axes_limits_not_forced_to_zero_horizontal():
    """
    Test that interactive horizontal SpanSelector does not force axes limits to include 0.
    
    This is a regression test for the bug where interactive SpanSelector
    incorrectly expanded axes limits to include x=0.
    """
    # Create figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same (not forced to include 0)
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector. This indicates the bug where "
        "axes limits are incorrectly forced to include 0."
    )
    
    plt.close(fig)


def test_spanselector_interactive_axes_limits_not_forced_to_zero_vertical():
    """
    Test that interactive vertical SpanSelector does not force axes limits to include 0.
    
    This is a regression test for the bug where interactive SpanSelector
    incorrectly expanded axes limits to include y=0.
    """
    # Create figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The y-limits should remain the same (not forced to include 0)
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} "
        "when creating interactive vertical SpanSelector. This indicates the bug where "
        "axes limits are incorrectly forced to include 0."
    )
    
    plt.close(fig)


def test_spanselector_non_interactive_axes_limits_unchanged():
    """
    Test that non-interactive SpanSelector also does not change axes limits.
    """
    # Create figure and axis with specific limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating non-interactive SpanSelector."
    )
    
    plt.close(fig)


if __name__ == "__main__":
    test_spanselector_interactive_axes_limits_not_forced_to_zero_horizontal()
    test_spanselector_interactive_axes_limits_not_forced_to_zero_vertical()
    test_spanselector_non_interactive_axes_limits_unchanged()
    print("All tests passed!")