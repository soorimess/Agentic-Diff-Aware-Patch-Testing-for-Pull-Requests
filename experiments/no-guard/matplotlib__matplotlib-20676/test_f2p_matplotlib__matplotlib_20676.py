"""
Tests for the SpanSelector axes limits bug.

This test checks that SpanSelector with interactive=True does not
incorrectly force the axes limits to include 0.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_spanselector_interactive_horizontal_does_not_force_zero_limits():
    """
    Test that interactive horizontal SpanSelector with initial data not including 0
    does not force axes x-limits to include 0.
    
    This tests the bug where interactive SpanSelector would expand axis limits
    to include 0, even when the axis data does not include 0.
    """
    # Create figure and axis with data that does not include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive horizontal SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after SpanSelector creation
    final_xlim = ax.get_xlim()
    
    # The x-limits should not have changed (should remain at (10, 20) + margins)
    # Prior to the fix, this would be false because limits would be forced to include 0
    assert initial_xlim == final_xlim, f"X-limits changed from {initial_xlim} to {final_xlim}"
    
    plt.close(fig)


def test_spanselector_interactive_vertical_does_not_force_zero_limits():
    """
    Test that interactive vertical SpanSelector with initial data not including 0
    does not force axes y-limits to include 0.
    
    This tests the bug where interactive SpanSelector would expand axis limits
    to include 0, even when the axis data does not include 0.
    """
    # Create figure and axis with data that does not include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive vertical SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after SpanSelector creation
    final_ylim = ax.get_ylim()
    
    # The y-limits should not have changed (should remain at (10, 20) + margins)
    # Prior to the fix, this would be false because limits would be forced to include 0  
    assert initial_ylim == final_ylim, f"Y-limits changed from {initial_ylim} to {final_ylim}"
    
    plt.close(fig)


def test_spanselector_interactive_with_specific_positive_data():
    """
    Test with data that is clearly positive (no zeros) 
    to ensure axes limits do not get expanded to include 0
    """
    fig, ax = plt.subplots()
    
    # Plot data that definitely doesn't contain zero values
    x_data = [5, 15, 25]
    y_data = [5, 15, 25]
    ax.plot(x_data, y_data)
    
    # Get initial axis bounds
    initial_xlim = ax.get_xlim()
    initial_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that x-limits haven't changed
    final_xlim = ax.get_xlim()
    final_ylim = ax.get_ylim()
    
    # X-limits should remain the same 
    assert initial_xlim == final_xlim, f"X-limits changed from {initial_xlim} to {final_xlim}"
    # Y-limits should also remain the same
    assert initial_ylim == final_ylim, f"Y-limits changed from {initial_ylim} to {final_ylim}"
    
    plt.close(fig)


def test_spanselector_non_interactive_still_works():
    """
    Test that non-interactive SpanSelector still works as expected.
    This is to make sure we're not over-testing.
    """
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    final_xlim = ax.get_xlim()
    
    # Non-interactive should also not change limits
    assert initial_xlim == final_xlim, f"X-limits changed from {initial_xlim} to {final_xlim}"
    
    plt.close(fig)


def test_spanselector_edge_case_zero_data():
    """
    Test edge case with data that includes zero to make sure it really
    doesn't force integer bounds inappropriately 
    """
    fig, ax = plt.subplots()
    ax.plot([-10, 10], [-10, 10])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get final x-limits
    final_xlim = ax.get_xlim()
    
    # X-limits should not have changed
    assert initial_xlim == final_xlim, f"X-limits changed from {initial_xlim} to {final_xlim}"
    
    plt.close(fig)