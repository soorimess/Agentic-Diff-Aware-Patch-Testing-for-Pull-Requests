"""
Regression test for matplotlib issue where interactive SpanSelector 
incorrectly forces axes limits to include 0.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector


def test_span_selector_interactive_axes_limits():
    """
    Test that interactive SpanSelector does not force axes limits to include 0.
    
    This is a regression test for the bug where interactive SpanSelector 
    would incorrectly expand axes limits to include x=0.
    """
    # Create figure and axis with non-zero limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda vmin, vmax: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The bug was that final_xlim would include 0, even though the data was [10, 20]
    # The fix should preserve the original limits
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} after creating SpanSelector. "
        "This indicates the bug where axes limits are incorrectly forced to include 0."
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical_axes_limits():
    """
    Test that interactive vertical SpanSelector does not force y axes limits to include 0.
    """
    # Create figure and axis with non-zero limits
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector
    ss = SpanSelector(ax, lambda vmin, vmax: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The bug was that final_ylim would include 0, even though the data was [10, 20]
    # The fix should preserve the original limits
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} after creating vertical SpanSelector. "
        "This indicates the bug where axes limits are incorrectly forced to include 0."
    )
    
    plt.close(fig)