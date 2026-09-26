"""
Test for matplotlib/matplotlib#20676
Bug: interactive SpanSelector incorrectly forces axes limits to include 0
"""
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np


def test_span_selector_interactive_axes_limits():
    """
    Test that interactive SpanSelector does not incorrectly force axes limits to include 0.
    
    This test reproduces the bug where creating an interactive SpanSelector 
    would cause the axes to be expanded to include 0, even when the data doesn't
    require it.
    """
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector - this should NOT modify the axes limits
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that axes limits haven't been modified to include 0
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same (10, 20) + margins
    # Before the fix, this would fail because axes limits would be expanded to include 0
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim}. "
        "This indicates the axes were incorrectly expanded to include 0."
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical_axes_limits():
    """
    Test that interactive vertical SpanSelector does not incorrectly force axes limits to include 0.
    """
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector - this should NOT modify the axes limits
    ss = widgets.SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Check that axes limits haven't been modified to include 0
    final_ylim = ax.get_ylim()
    
    # The y-limits should remain the same (10, 20) + margins
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim}. "
        "This indicates the axes were incorrectly expanded to include 0."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits():
    """
    Test that non-interactive SpanSelector behaves correctly (control test).
    """
    # Create a figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector - this should also NOT modify the axes limits
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Check that axes limits haven't been modified
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim}. "
        "This indicates the axes were incorrectly modified."
    )
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_data():
    """
    Test that interactive SpanSelector works correctly when data includes 0.
    """
    # Create a figure and axis with data that includes 0
    fig, ax = plt.subplots()
    ax.plot([-10, 10], [-10, 10])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector - this should NOT modify the axes limits
    ss = widgets.SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that axes limits haven't been modified to include 0
    final_xlim = ax.get_xlim()
    
    # The x-limits should remain the same
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim}. "
        "This indicates the axes were incorrectly expanded."
    )
    
    plt.close(fig)