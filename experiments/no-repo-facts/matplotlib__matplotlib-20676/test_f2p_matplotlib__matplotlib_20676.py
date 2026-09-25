import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_span_selector_interactive_horizontal_forces_zero_limits():
    """Test that interactive horizontal SpanSelector doesn't incorrectly force axes limits to include 0."""
    
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_x_limits = ax.get_xlim()
    
    # Create interactive horizontal span selector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating span selector
    final_x_limits = ax.get_xlim()
    
    # Close the figure to avoid display issues
    plt.close(fig)
    
    # The bug: x-limits are expanded to include 0
    # The fix: x-limits should remain unchanged
    assert initial_x_limits == final_x_limits, (
        f"X-limits changed from {initial_x_limits} to {final_x_limits}. "
        "Interactive horizontal SpanSelector incorrectly forces axes limits to include 0."
    )


def test_span_selector_interactive_vertical_preserves_limits():
    """Test that interactive vertical SpanSelector doesn't incorrectly force axes limits to include 0."""
    
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_y_limits = ax.get_ylim()
    
    # Create interactive vertical span selector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating span selector
    final_y_limits = ax.get_ylim()
    
    # Close the figure to avoid display issues
    plt.close(fig)
    
    # The bug: y-limits are expanded to include 0
    # The fix: y-limits should remain unchanged
    assert initial_y_limits == final_y_limits, (
        f"Y-limits changed from {initial_y_limits} to {final_y_limits}. "
        "Interactive vertical SpanSelector incorrectly forces axes limits to include 0."
    )


def test_span_selector_non_interactive_preserves_limits():
    """Test that non-interactive SpanSelector also doesn't change limits."""
    
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_x_limits = ax.get_xlim()
    
    # Create non-interactive span selector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Get x-limits after creating span selector
    final_x_limits = ax.get_xlim()
    
    # Close the figure to avoid display issues
    plt.close(fig)
    
    # X-limits should remain unchanged
    assert initial_x_limits == final_x_limits, (
        f"X-limits changed from {initial_x_limits} to {final_x_limits}. "
        "Non-interactive SpanSelector incorrectly changes axes limits."
    )


if __name__ == "__main__":
    test_span_selector_interactive_horizontal_forces_zero_limits()
    test_span_selector_interactive_vertical_preserves_limits() 
    test_span_selector_non_interactive_preserves_limits()
    print("All tests passed!")