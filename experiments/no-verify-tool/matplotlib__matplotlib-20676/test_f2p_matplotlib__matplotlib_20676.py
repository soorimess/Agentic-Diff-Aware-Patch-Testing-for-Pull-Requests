"""
Test for matplotlib bug #20676.

The bug is that interactive SpanSelector incorrectly forces axes limits to include 0.

When creating an interactive SpanSelector on axes that do not already have 0 
in their x-limits, the x-limits are incorrectly modified to include 0.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector


def test_span_selector_interactive_preserves_axes_limits():
    """
    Test that interactive SpanSelector does not modify axes limits.
    
    Before the fix: When interactive=True, the X-axis limits got 
    incorrectly expanded to include 0 even if the original data didn't include 0.
    
    After the fix: X-axis limits should remain exactly as they were before
    creating the interactive SpanSelector.
    """
    # Create figure and axis with specific data that doesn't include 0  
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits before SpanSelector creation
    initial_xlim = ax.get_xlim()
    print(f"Initial xlim: {initial_xlim}")
    
    # Create interactive SpanSelector  
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check x-limits after creating SpanSelector
    xlim_after = ax.get_xlim()
    print(f"Xlim after creating SpanSelector: {xlim_after}")
    
    # The fix ensures that the limits are not changed
    assert xlim_after == initial_xlim, (
        f"Interactive SpanSelector changed x-limits from {initial_xlim} to {xlim_after}. "
        "This should not happen according to the fix for matplotlib issue #20676."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_no_change():
    """
    Test that non-interactive SpanSelector doesn't change axes limits.    
    """
    # Create figure and axis with specific data that doesn't include 0  
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    print(f"Initial xlim (non-interactive): {initial_xlim}")
    
    # Create non-interactive SpanSelector - this should not affect limits
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Check x-limits after creating SpanSelector 
    xlim_after = ax.get_xlim()
    print(f"Xlim after creating non-interactive SpanSelector: {xlim_after}")
    
    # X-limits should be the same
    assert xlim_after == initial_xlim, (
        f"Non-interactive SpanSelector changed x-limits from {initial_xlim} to {xlim_after}. "
        "Non-interactive SpanSelector should preserve axes limits."
    )
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_data_preserves_limits():
    """
    Test that interactive SpanSelector with data that includes 0 behaves correctly.
    """
    # Create figure and axis with data that includes 0  
    fig, ax = plt.subplots()
    ax.plot([-20, 0, 10], [10, 0, 20])  # This includes 0
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    print(f"Initial xlim (with zero): {initial_xlim}")
    
    # Create interactive SpanSelector 
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check x-limits after creating SpanSelector
    xlim_after = ax.get_xlim()
    print(f"Xlim after creating SpanSelector (with zero): {xlim_after}")
    
    # Should preserve the original limits even if they include 0
    assert xlim_after == initial_xlim, (
        f"Interactive SpanSelector changed x-limits from {initial_xlim} to {xlim_after} "
        "when data already includes 0."
    )
    
    plt.close(fig)