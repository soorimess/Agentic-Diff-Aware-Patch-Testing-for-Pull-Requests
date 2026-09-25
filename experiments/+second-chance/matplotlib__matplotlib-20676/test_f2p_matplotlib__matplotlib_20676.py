"""
Regression test for SpanSelector interactive mode bug where axes limits
incorrectly include 0.

Before the fix: interactive SpanSelector would expand axes limits to include 0
After the fix: interactive SpanSelector preserves axes limits as they were
"""
import pytest
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_spanselector_interactive_preserves_axis_limits_horizontal():
    """
    Test that interactive horizontal SpanSelector does not force axis limits to include 0.
    
    This is a regression test for the bug where interactive SpanSelector 
    would incorrectly expand axis limits to include 0, even when they 
    originally did not.
    """
    # Create a plot with specific limits that don't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get the original x-limits (should be around (10, 20) + margins)
    original_xlim = ax.get_xlim()
    
    # Create interactive horizontal SpanSelector - this should NOT modify axis limits
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that x-limits remain unchanged (confirming that 0 isn't forced in)
    new_xlim = ax.get_xlim()
    
    # The core issue: axis should NOT have its lower limit forced to be 0
    # This is the key assertion - the lower limit should not change to 0
    assert not (new_xlim[0] == 0.0), (
        "X-limits were incorrectly expanded to include 0.0. "
        f"Original: {original_xlim}, New: {new_xlim}"
    )
    
    # Check that upper limit is preserved
    assert new_xlim[1] == original_xlim[1], (
        f"Upper X-limit changed from {original_xlim[1]} to {new_xlim[1]}"
    )
    
    plt.close(fig)


def test_spanselector_interactive_preserves_axis_limits_vertical():
    """
    Test that interactive vertical SpanSelector does not force axis limits to include 0.
    """
    # Create a plot with specific limits that don't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get the original y-limits (should be around (10, 20) + margins)
    original_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector - this should NOT modify axis limits  
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Check that y-limits remain unchanged (confirming that 0 isn't forced in)
    new_ylim = ax.get_ylim()
    
    # The core issue: axis should NOT have its lower limit forced to be 0
    assert not (new_ylim[0] == 0.0), (
        "Y-limits were incorrectly expanded to include 0.0. "
        f"Original: {original_ylim}, New: {new_ylim}"
    )
    
    # Check that upper limit is preserved
    assert new_ylim[1] == original_ylim[1], (
        f"Upper Y-limit changed from {original_ylim[1]} to {new_ylim[1]}"
    )
    
    plt.close(fig)


def test_spanselector_interactive_bounds_preservation():
    """
    Test that when axes already have limits that don't include 0,
    interactive span selector preserves the exact bounds.
    """
    fig, ax = plt.subplots()
    
    # Set custom axis limits  
    ax.set_xlim(5, 15)
    ax.set_ylim(2, 8)
    
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that both x and y limits are preserved
    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()
    
    assert new_xlim == original_xlim, (
        f"X-limits changed from {original_xlim} to {new_xlim}"
    )
    assert new_ylim == original_ylim, (
        f"Y-limits changed from {original_ylim} to {new_ylim}"
    )
    
    plt.close(fig)