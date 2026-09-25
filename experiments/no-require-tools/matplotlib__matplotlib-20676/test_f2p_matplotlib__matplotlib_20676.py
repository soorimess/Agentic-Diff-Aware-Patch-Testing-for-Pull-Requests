"""
Regression test for matplotlib/matplotlib#20676
SpanSelector incorrectly forces axes limits to include 0 when interactive=True
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import numpy as np
import pytest


def test_span_selector_interactive_horizontal_preserves_axes_limits():
    """
    Test that SpanSelector with interactive=True and horizontal direction 
    does not modify axes limits to include 0 unnecessarily.
    """
    # Create figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])  # Data range is [10, 20] for both x and y
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create a SpanSelector with interactive=True and horizontal direction
    ss = mwidgets.SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Check that the axes limits have NOT changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x and y bounds should remain exactly the same
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound} - this is the bug!"
    )
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound} - this is the bug!"
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical_preserves_axes_limits():
    """
    Test that SpanSelector with interactive=True and vertical direction
    does not modify axes limits to include 0 unnecessarily.
    """
    # Create figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])  # Data range is [10, 20] for both x and y
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create a SpanSelector with interactive=True and vertical direction
    ss = mwidgets.SpanSelector(ax, lambda v1, v2: None, "vertical", interactive=True)
    
    # Check that the axes limits have NOT changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x and y bounds should remain exactly the same
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound} - this is the bug!"
    )
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound} - this is the bug!"
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_preserves_axes_limits():
    """
    Test that SpanSelector with interactive=False also preserves axes limits.
    This ensures we're testing the right behavior.
    """
    # Create figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])  # Data range is [10, 20] for both x and y
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create a SpanSelector with interactive=False 
    ss = mwidgets.SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=False)
    
    # Check that the axes limits have NOT changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x and y bounds should remain exactly the same
    assert initial_xbound == final_xbound
    assert initial_ybound == final_ybound
    
    plt.close(fig)


def test_span_selector_interactive_with_zero_data():
    """
    Test that even with data that includes zero, the behavior is correct.
    """
    # Create figure with axes that have data that spans 0
    fig, ax = plt.subplots()
    ax.plot([-10, 10], [-10, 10])  # Data range includes 0
    
    # Get initial bounds
    initial_xbound = ax.get_xbound()
    initial_ybound = ax.get_ybound()
    
    # Create a SpanSelector with interactive=True
    ss = mwidgets.SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Check that the axes limits have NOT changed
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x and y bounds should remain exactly the same
    assert initial_xbound == final_xbound, (
        f"X-axis bounds changed from {initial_xbound} to {final_xbound}"
    )
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound}"
    )
    
    plt.close(fig)


def test_span_selector_interactive_axbound_includes_zero():
    """
    Test the specific buggy case: when xbound includes 0 but the data does not.
    """
    # Create figure with axes where bounds include 0 but data does not
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Force the x-axis bounds to include zero (this should NOT happen in the fix)
    # but we will check this to make sure it's the issue scenario
    ax.set_xlim(-5, 30)
    
    # Get initial bounds
    initial_xbound = ax.get_xbound() 
    initial_ybound = ax.get_ybound()
    
    # Create a SpanSelector with interactive=True - this is when the bug manifests
    ss = mwidgets.SpanSelector(ax, lambda v1, v2: None, "horizontal", interactive=True)
    
    # Check that the axes limits have NOT changed (this is the assertion we're testing)
    final_xbound = ax.get_xbound()
    final_ybound = ax.get_ybound()
    
    # The x and y bounds should remain exactly the same - verify this is true
    assert initial_xbound == final_xbound, (
        f"BUG: X-axis bounds changed from {initial_xbound} to {final_xbound} "
        f"when they should have remained unchanged!"
    )
    assert initial_ybound == final_ybound, (
        f"Y-axis bounds changed from {initial_ybound} to {final_ybound}" 
    )
    
    plt.close(fig)