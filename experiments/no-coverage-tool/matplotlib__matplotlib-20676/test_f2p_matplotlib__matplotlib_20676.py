"""
Regression test for SpanSelector interactive mode incorrectly forcing axes limits to include 0.

This test ensures that when SpanSelector is created with interactive=True, 
the x-limits (or y-limits) of the axis are not incorrectly expanded to include 0,
especially when the original data doesn't include 0.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np
import pytest


def test_span_selector_interactive_preserves_xlimits():
    """Test that interactive SpanSelector preserves original x-limits without including 0."""
    # Create a plot with data that excludes 0 on x-axis
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store the original x-limits
    original_xlim = ax.get_xlim()
    
    # Create interactive span selector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that x-limits haven't been changed to include 0
    new_xlim = ax.get_xlim()
    
    # The x-limits should be the same as original 
    # Before the fix, especially when data doesn't include 0,
    # the x-limits would be expanded to include 0 due to get_xbound()
    assert new_xlim == original_xlim, f"X-limits changed from {original_xlim} to {new_xlim}"
    
    plt.close(fig)


def test_span_selector_interactive_preserves_ylimits():
    """Test that interactive SpanSelector preserves original y-limits without including 0."""
    # Create a plot with data that excludes 0 on y-axis
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store the original y-limits
    original_ylim = ax.get_ylim()
    
    # Create interactive span selector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Check that y-limits haven't been changed to include 0
    new_ylim = ax.get_ylim()
    
    # The y-limits should be the same as original 
    # Before the fix, especially when data doesn't include 0,
    # the y-limits would be expanded to include 0 due to get_ybound()
    assert new_ylim == original_ylim, f"Y-limits changed from {original_ylim} to {new_ylim}"
    
    plt.close(fig)


def test_span_selector_non_interactive_unchanged():
    """Test that non-interactive SpanSelector behavior is unchanged."""
    # Create a plot with data that excludes 0 on x-axis
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store the original x-limits
    original_xlim = ax.get_xlim()
    
    # Create non-interactive span selector (should not affect limits)
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Check that x-limits haven't been changed
    new_xlim = ax.get_xlim()
    
    # The x-limits should be the same as original
    assert new_xlim == original_xlim, f"X-limits changed from {original_xlim} to {new_xlim}"
    
    plt.close(fig)


def test_span_selector_with_zero_in_data():
    """Test that SpanSelector handles data that includes 0 correctly."""
    # Create a plot with data that includes 0 on x-axis
    fig, ax = plt.subplots()
    ax.plot([-5, 0, 5], [10, 10, 10])
    
    # Store the original x-limits
    original_xlim = ax.get_xlim()
    
    # Create interactive span selector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that x-limits haven't been changed unnecessarily
    new_xlim = ax.get_xlim()
    
    # The x-limits should be preserved (even if they include 0 now)
    assert new_xlim == original_xlim, f"X-limits changed from {original_xlim} to {new_xlim}"
    
    plt.close(fig)