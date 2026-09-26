"""
Regression test for matplotlib issue where interactive SpanSelector
incorrectly forces axes limits to include 0.

This test ensures that when creating an interactive SpanSelector, the
axes limits are not incorrectly expanded to include 0.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


def test_span_selector_interactive_horizontal_axes_limits_not_expanded_to_zero():
    """
    Test that interactive horizontal SpanSelector does not force axes limits to include 0.
    
    Before the fix, when creating an interactive SpanSelector, the axes
    limits would be expanded to include 0, even if they didn't previously.
    """
    # Create a figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector - this should NOT modify the axes limits
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The limits should remain the same (not expanded to include 0)
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_vertical_axes_limits_not_expanded_to_zero():
    """
    Test that interactive vertical SpanSelector does not force axes limits to include 0.
    
    Before the fix, when creating an interactive SpanSelector, the axes
    limits would be expanded to include 0, even if they didn't previously.
    """
    # Create a figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector - this should NOT modify the axes limits
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Get y-limits after creating SpanSelector
    final_ylim = ax.get_ylim()
    
    # The limits should remain the same (not expanded to include 0)
    assert initial_ylim == final_ylim, (
        f"Y-limits changed from {initial_ylim} to {final_ylim} "
        "when creating interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_non_interactive_axes_limits_unchanged():
    """
    Test that non-interactive SpanSelector does not modify axes limits.
    
    This is a control test to ensure the behavior is correct for non-interactive mode.
    """
    # Create a figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create non-interactive SpanSelector - this should NOT modify the axes limits
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=False)
    
    # Get x-limits after creating SpanSelector
    final_xlim = ax.get_xlim()
    
    # The limits should remain the same
    assert initial_xlim == final_xlim, (
        f"X-limits changed from {initial_xlim} to {final_xlim} "
        "when creating non-interactive SpanSelector"
    )
    
    plt.close(fig)


def test_span_selector_interactive_edge_handles_initial_positions_horizontal():
    """
    Test that the initial positions of horizontal edge handles are correct.
    
    This test specifically checks that the edge handles are initialized with
    the correct positions based on the current axis bounds, not forcing 0.
    """
    # Create a figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial x-limits
    initial_xlim = ax.get_xlim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "horizontal", interactive=True)
    
    # Check that the edge handles were initialized with the correct positions
    # (they should use the current axis bounds, not force 0)
    if hasattr(ss, '_edge_handles') and ss._edge_handles is not None:
        positions = ss._edge_handles.positions
        # The positions should be based on the current axis bounds, not forced to include 0
        # For horizontal, we expect positions to be [xlim[0], xlim[1]] or similar bounds
        assert len(positions) == 2, f"Expected 2 positions, got {len(positions)}"
        # The positions should not be [0, 0] unless the axis already includes 0
        if 0 in initial_xlim:
            # If 0 is already in the limits, it's OK
            assert 0 in positions or (positions[0] == positions[1] and positions[0] == 0)
        else:
            # If 0 is not in the limits, positions should not include 0
            assert 0 not in positions, (
                f"Edge handles initialized with 0 positions {positions} "
                f"when axis limits are {initial_xlim}"
            )
    
    plt.close(fig)


def test_span_selector_interactive_edge_handles_initial_positions_vertical():
    """
    Test that the initial positions of vertical edge handles are correct.
    
    This test specifically checks that the edge handles are initialized with
    the correct positions based on the current axis bounds, not forcing 0.
    """
    # Create a figure with axes that have limits not including 0
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    
    # Get initial y-limits
    initial_ylim = ax.get_ylim()
    
    # Create interactive SpanSelector
    ss = SpanSelector(ax, lambda x, y: None, "vertical", interactive=True)
    
    # Check that the edge handles were initialized with the correct positions
    # (they should use the current axis bounds, not force 0)
    if hasattr(ss, '_edge_handles') and ss._edge_handles is not None:
        positions = ss._edge_handles.positions
        # The positions should be based on the current axis bounds, not forced to include 0
        assert len(positions) == 2, f"Expected 2 positions, got {len(positions)}"
        # The positions should not be [0, 0] unless the axis already includes 0
        if 0 in initial_ylim:
            # If 0 is already in the limits, it's OK
            assert 0 in positions or (positions[0] == positions[1] and positions[0] == 0)
        else:
            # If 0 is not in the limits, positions should not include 0
            assert 0 not in positions, (
                f"Edge handles initialized with 0 positions {positions} "
                f"when axis limits are {initial_ylim}"
            )
    
    plt.close(fig)