"""
Test for SpanSelector interactive mode bug where axes limits are incorrectly
expanded to include 0.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_span_selector_interactive_axes_limits_horizontal():
    """Test that interactive SpanSelector doesn't force axes limits to include 0 (horizontal)."""
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The bug: axes limits are expanded to include 0
    # The fix: axes limits should remain the same
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_axes_limits_vertical():
    """Test that interactive SpanSelector doesn't force axes limits to include 0 (vertical)."""
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector in vertical direction
    ss = SpanSelector(ax, lambda v1, v2: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The bug: axes limits are expanded to include 0
    # The fix: axes limits should remain the same
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} "
        "when creating interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits():
    """Test that non-interactive SpanSelector doesn't change axes limits."""
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector
    ss = SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=False)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # Non-interactive should not change limits
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating non-interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_data():
    """Test that interactive SpanSelector works correctly with data that includes 0."""
    # Create a figure and axis with data that includes 0
    fig, ax = plt.subplots()
    ax.plot([-10, 10], [-10, 10])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # Should not change limits
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector with data including 0"
    )
    
    plt.close(fig)


def test_span_selector_explicit_zero_bounds():
    """Test that interactive SpanSelector doesn't force axes limits to include 0 when axis bounds include 0."""
    # Create a figure and axis with explicit axis bounds that include 0
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 15)  # This should not be changed by interactive span selector
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # Should not change limits even if axis bounds include 0
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector with axis bounds that include 0"
    )
    
    plt.close(fig)