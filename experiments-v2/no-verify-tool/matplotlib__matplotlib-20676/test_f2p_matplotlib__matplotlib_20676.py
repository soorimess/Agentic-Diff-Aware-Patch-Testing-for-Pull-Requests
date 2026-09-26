"""
Test for SpanSelector interactive mode bug where axes limits are incorrectly
forced to include 0.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector


def test_spanselector_interactive_axes_limits():
    """
    Test that SpanSelector with interactive=True does not force axes limits to include 0.
    
    This is a regression test for matplotlib/matplotlib#20676.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store original axis bounds
    orig_xbound = ax.get_xbound()
    orig_ybound = ax.get_ybound()
    
    # Create SpanSelector with interactive=True
    ss = SpanSelector(ax, lambda vmin, vmax: None, "horizontal", interactive=True)
    
    # Check if axis bounds were modified
    new_xbound = ax.get_xbound()
    new_ybound = ax.get_ybound()
    
    # The bug was that xbounds would be modified to include 0
    # This should not happen with the original data range [10, 20]
    assert orig_xbound == new_xbound, (
        f"X-axis bounds changed from {orig_xbound} to {new_xbound}. "
        "Axes limits should not be forced to include 0."
    )
    
    assert orig_ybound == new_ybound, (
        f"Y-axis bounds changed from {orig_ybound} to {new_ybound}. "
        "Axes limits should not be forced to include 0."
    )
    
    plt.close(fig)


def test_spanselector_interactive_axes_limits_vertical():
    """
    Test that SpanSelector with interactive=True and vertical direction 
    does not force axes limits to include 0.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store original axis bounds
    orig_xbound = ax.get_xbound()
    orig_ybound = ax.get_ybound()
    
    # Create SpanSelector with interactive=True and vertical direction
    ss = SpanSelector(ax, lambda vmin, vmax: None, "vertical", interactive=True)
    
    # Check if axis bounds were modified
    new_xbound = ax.get_xbound()
    new_ybound = ax.get_ybound()
    
    # The bug was that ybounds would be modified to include 0
    # This should not happen with the original data range [10, 20]
    assert orig_xbound == new_xbound, (
        f"X-axis bounds changed from {orig_xbound} to {new_xbound}. "
        "Axes limits should not be forced to include 0."
    )
    
    assert orig_ybound == new_ybound, (
        f"Y-axis bounds changed from {orig_ybound} to {new_ybound}. "
        "Axes limits should not be forced to include 0."
    )
    
    plt.close(fig)


def test_spanselector_non_interactive_no_change():
    """
    Test that SpanSelector with interactive=False does not change axes limits.
    """
    # Create figure and axis with data that doesn't include 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Store original axis bounds
    orig_xbound = ax.get_xbound()
    orig_ybound = ax.get_ybound()
    
    # Create SpanSelector with interactive=False
    ss = SpanSelector(ax, lambda vmin, vmax: None, "horizontal", interactive=False)
    
    # Check if axis bounds were modified
    new_xbound = ax.get_xbound()
    new_ybound = ax.get_ybound()
    
    # With interactive=False, no change should occur
    assert orig_xbound == new_xbound, (
        f"X-axis bounds changed from {orig_xbound} to {new_xbound}. "
        "Axes limits should not be forced to include 0."
    )
    
    assert orig_ybound == new_ybound, (
        f"Y-axis bounds changed from {orig_ybound} to {new_ybound}. "
        "Axes limits should not be forced to include 0."
    )
    
    plt.close(fig)