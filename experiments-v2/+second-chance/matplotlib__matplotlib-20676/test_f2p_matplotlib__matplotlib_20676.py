"""
Regression test for matplotlib/matplotlib#20676
Interactive SpanSelector incorrectly forces axes limits to include 0
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_span_selector_interactive_axes_limits():
    """
    Test that interactive SpanSelector does not force axes limits to include 0.
    
    Before the fix, when creating an interactive SpanSelector, the axes limits
    would be expanded to include 0 even when the data doesn't contain 0.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same (not expanded to include 0)
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim}. "
        "Interactive SpanSelector incorrectly forced axes limits to include 0."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits():
    """
    Test that non-interactive SpanSelector does not affect axes limits.
    """
    # Create figure and axis with data that doesn't include 0
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
        f"X-limits changed from {initial_xlim} to {final_xlim}. "
        "Non-interactive SpanSelector incorrectly affected axes limits."
    )
    
    plt.close(fig)


def test_span_selector_interactive_y_axis():
    """
    Test that interactive SpanSelector does not force y-axes limits to include 0.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The y-limits should remain the same (not expanded to include 0)
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim}. "
        "Interactive SpanSelector incorrectly forced axes limits to include 0."
    )
    
    plt.close(fig)