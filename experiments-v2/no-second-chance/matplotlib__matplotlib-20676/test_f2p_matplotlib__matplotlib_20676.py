"""
Regression test for SpanSelector interactive mode incorrectly forcing axes limits to include 0.

This test ensures that when SpanSelector is used with interactive=True, 
the axes limits are not incorrectly expanded to include 0.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np


def test_span_selector_interactive_horizontal_axes_limits():
    """
    Test that interactive horizontal SpanSelector does not force axes limits to include 0.
    
    Before the fix, when using interactive=True with SpanSelector, 
    the axes x-limits would be expanded to include x=0 even when the data
    doesn't require it.
    """
    # Create a figure and axis with data that doesn't include x=0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain unchanged
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical_axes_limits():
    """
    Test that interactive vertical SpanSelector does not force axes limits to include 0.
    
    Before the fix, when using interactive=True with SpanSelector, 
    the axes y-limits would be expanded to include y=0 even when the data
    doesn't require it.
    """
    # Create a figure and axis with data that doesn't include y=0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector
    ss = widgets.SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The y-limits should remain unchanged
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} "
        "when creating interactive vertical SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits():
    """
    Test that non-interactive SpanSelector does not affect axes limits.
    """
    # Create a figure and axis with data that doesn't include x=0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain unchanged
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating non-interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_data():
    """
    Test that interactive SpanSelector behaves correctly when data includes 0.
    """
    # Create a figure and axis with data that includes x=0
    fig, ax = plt.subplots()
    ax.plot([-10, 0, 10], [10, 0, 10])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain unchanged
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector with data including 0"
    )
    
    plt.close(fig)