"""
Test for SpanSelector interactive mode incorrectly forcing axes limits to include 0.

This regression test ensures that when SpanSelector is used in interactive mode,
it doesn't expand the axes limits to include 0, which happened in matplotlib 3.5.0.
"""
import pytest
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import SpanSelector


def test_span_selector_interactive_does_not_force_zero_bounds():
    """
    Test that interactive SpanSelector does not change axis bounds to include 0.
    
    Previously, when SpanSelector was created with interactive=True, it would call
    get_xbound() or get_ybound() to determine initial positions for edge handles,
    which would expand the bounds to include 0 even when the data didn't require it.
    """
    # Create a plot with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial bounds before creating SpanSelector
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create SpanSelector in interactive mode
    ss = SpanSelector(ax, lambda x: None, "horizontal", interactive=True)
    
    # Check that bounds haven't changed to include 0
    new_xbound = ax.get_xbound()
    new_ybound = ax.get_ybound()
    
    # The x bounds should be unchanged
    assert new_xbound == initial_xbound, (
        f"X bounds changed from {initial_xbound} to {new_xbound}. "
        "SpanSelector should not force bounds to include 0."
    )
    
    # The y bounds should be unchanged  
    assert new_ybound == initial_ybound, (
        f"Y bounds changed from {initial_ybound} to {new_ybound}. "
        "SpanSelector should not force bounds to include 0."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_unchanged():
    """
    Test that non-interactive SpanSelector behavior remains the same.
    """
    # Create a plot with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    
    # Create SpanSelector in non-interactive mode
    ss = SpanSelector(ax, lambda x: None, "horizontal", interactive=False)
    
    # Bounds should still be unchanged
    new_xbound = ax.get_xbound()
    
    assert new_xbound == initial_xbound, (
        "Non-interactive SpanSelector should not change x bounds."
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical():
    """
    Test that interactive vertical SpanSelector also doesn't force zero bounds.
    """
    # Create a plot with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create vertical SpanSelector in interactive mode
    ss = SpanSelector(ax, lambda x: None, "vertical", interactive=True)
    
    # Check that bounds haven't changed
    new_xbound = ax.get_xbound()
    new_ybound = ax.get_ybound()
    
    assert new_xbound == initial_xbound, (
        "Vertical SpanSelector should not change x bounds."
    )
    
    assert new_ybound == initial_ybound, (
        "Vertical SpanSelector should not change y bounds."
    )
    
    plt.close(fig)