"""
Regression test for bug where interactive SpanSelector incorrectly 
forces axes limits to include 0.

This test ensures that when creating an interactive SpanSelector on axes
that have data not including 0, the axes limits are not arbitrarily 
expanded to include 0.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.testing.widgets import do_event


def test_span_selector_interactive_no_force_zero_xlims():
    """
    Test that interactive SpanSelector does not force x-axis limits to include 0.
    
    When creating an interactive SpanSelector, the widget should not modify 
    the axes limits to include 0 if the data doesn't include 0.
    """
    # Create figure and axes with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial axis limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    def onselect(start, end):
        pass
    
    ss = widgets.SpanSelector(ax, onselect, "horizontal", interactive=True)
    
    # Check that axis limits have not been modified to include 0
    final_xlim = ax.get_xlim()
    
    # The limits should be unchanged (or at least not forced to include 0)
    # The original data was [10, 20], so limits should be around that range
    assert initial_xlim == final_xlim, (
        f"X-axis limits changed from {initial_xlim} to {final_xlim}. "
        "SpanSelector should not force limits to include 0."
    )
    
    plt.close(fig)


def test_span_selector_interactive_no_force_zero_ylim():
    """
    Test that interactive SpanSelector does not force y-axis limits to include 0.
    
    When creating an interactive SpanSelector, the widget should not modify 
    the axes limits to include 0 if the data doesn't include 0.
    """
    # Create figure and axes with data that doesn't include 0  
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial axis limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector
    def onselect(start, end):
        pass
        
    ss = widgets.SpanSelector(ax, onselect, "vertical", interactive=True)
    
    # Check that axis limits have not been modified to include 0
    final_ylim = ax.get_ylim()
    
    # The limits should be unchanged (or at least not forced to include 0)
    assert initial_ylim == final_ylim, (
        f"Y-axis limits changed from {initial_ylim} to {final_ylim}. "
        "SpanSelector should not force limits to include 0."
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_unchanged():
    """
    Test that non-interactive SpanSelector behavior is unchanged.
    
    This is to ensure we're not breaking non-interactive behavior.
    """
    # Create figure and axes with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial axis limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector
    def onselect(start, end):
        pass
        
    ss = widgets.SpanSelector(ax, onselect, "horizontal", interactive=False)
    
    # Check that axis limits have not been modified to include 0
    final_xlim = ax.get_xlim()
    
    # The limits should be unchanged
    assert initial_xlim == final_xlim, (
        f"X-axis limits changed from {initial_xlim} to {final_xlim}. "
        "Non-interactive SpanSelector should not affect limits."
    )
    
    plt.close(fig)


def test_span_selector_zero_data_preserved():
    """
    Test that when data includes 0, axes limits should be able to include 0.
    
    This tests the case where data naturally includes 0, which should be allowed.
    """
    # Create figure and axes with data that includes 0
    fig, ax = plt.subplots()
    ax.plot([-10, 0, 10], [-10, 0, 10])  # Data includes 0
    
    # Get initial axis limits 
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    def onselect(start, end):
        pass
    
    ss = widgets.SpanSelector(ax, onselect, "horizontal", interactive=True)
    
    # Check that axis limits have not been modified (this is testing that we don't change
    # behavior unnecessarily when 0 is naturally part of the data)
    final_xlim = ax.get_xlim()
    
    assert initial_xlim == final_xlim, (
        f"X-axis limits changed from {initial_xlim} to {final_xlim}. "
        "Limits should remain consistent when 0 is naturally part of the data."
    )
    
    plt.close(fig)