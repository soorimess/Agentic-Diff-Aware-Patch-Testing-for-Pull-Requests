"""
Regression test for matplotlib bug where interactive SpanSelector 
incorrectly forces axes limits to include 0.

This test ensures that when creating an interactive SpanSelector on axes
that don't include 0, the axes limits remain unchanged.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
import pytest


def test_span_selector_interactive_axes_limits_not_expanded_to_zero():
    """
    Test that interactive SpanSelector does not force axes limits to include 0.
    
    When creating an interactive SpanSelector on axes that don't include 0,
    the axes limits should remain unchanged. Previously, this would incorrectly
    expand the axes limits to include 0 due to a bug in _setup_edge_handle.
    """
    # Create figure and axes with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial axis bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda vmin, vmax: None, "horizontal", 
                              interactive=True)
    
    # Check that axis bounds have not been changed to include 0
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x-axis bounds should remain the same (not expanded to include 0)
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound}. "
        "Axes limits should not be forced to include 0."
    )
    
    # The y-axis bounds should remain the same
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound}. "
        "Y-axis bounds should not be affected."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits_unchanged():
    """
    Test that non-interactive SpanSelector also doesn't change axes limits.
    """
    # Create figure and axes with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial axis bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create non-interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda vmin, vmax: None, "horizontal", 
                              interactive=False)
    
    # Check that axis bounds have not been changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The axis bounds should remain the same
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound}. "
        "Axes limits should not be changed."
    )
    
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound}. "
        "Y-axis bounds should not be affected."
    )
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_in_data():
    """
    Test that interactive SpanSelector works correctly when data includes 0.
    """
    # Create figure and axes with data that includes 0
    fig, ax = plt.subplots()
    ax.plot([-10, 0, 10], [10, 0, 10])
    
    # Get initial axis bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create interactive SpanSelector
    ss = widgets.SpanSelector(ax, lambda vmin, vmax: None, "horizontal", 
                              interactive=True)
    
    # Check that axis bounds have not been changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The axis bounds should remain the same
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound}. "
        "Axes limits should not be changed."
    )
    
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound}. "
        "Y-axis bounds should not be affected."
    )
    
    plt.close(fig)