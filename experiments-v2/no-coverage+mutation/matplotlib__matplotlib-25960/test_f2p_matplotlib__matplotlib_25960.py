import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.transforms import Bbox


def test_subfigures_wspace_hspace_no_layout_engine():
    """Test that wspace and hspace parameters are properly applied when no layout engine is used."""
    # Create a figure without a layout engine (this is the key case that was broken)
    fig = plt.figure(figsize=(10, 10))
    fig.set_layout_engine(None)  # Explicitly disable layout engine
    
    # Create subfigures with non-zero wspace and hspace
    subfigs_with_spacing = fig.subfigures(2, 2, wspace=0.2, hspace=0.3)
    
    # Create subfigures with zero wspace and hspace for comparison
    fig2 = plt.figure(figsize=(10, 10))
    fig2.set_layout_engine(None)
    subfigs_no_spacing = fig2.subfigures(2, 2, wspace=0, hspace=0)
    
    # Get the bounding boxes of the subfigures
    bboxes_with_spacing = []
    bboxes_no_spacing = []
    
    for row in subfigs_with_spacing:
        for subfig in row:
            bboxes_with_spacing.append(subfig.get_window_extent())
    
    for row in subfigs_no_spacing:
        for subfig in row:
            bboxes_no_spacing.append(subfig.get_window_extent())
    
    # With wspace=0.2 and hspace=0.3, the subfigures should be more spread out
    # than with wspace=0 and hspace=0
    
    # Check that we have 4 subfigures in each case
    assert len(bboxes_with_spacing) == 4
    assert len(bboxes_no_spacing) == 4
    
    # Extract positions for comparison
    positions_with_spacing = [(bbox.x0, bbox.y0, bbox.x1, bbox.y1) for bbox in bboxes_with_spacing]
    positions_no_spacing = [(bbox.x0, bbox.y0, bbox.x1, bbox.y1) for bbox in bboxes_no_spacing]
    
    # The key assertion: With proper spacing, the positions should be different
    # In the buggy version, both would have identical positions because wspace/hspace
    # were ignored when layout_engine is None
    unique_positions_with_spacing = set(positions_with_spacing)
    unique_positions_no_spacing = set(positions_no_spacing)
    
    # This test specifically checks that the spacing parameters are actually applied
    # When they work correctly, we should see different positions
    assert len(unique_positions_with_spacing) > 1, "With wspace=0.2 and hspace=0.3, subfigures should have multiple positions"
    
    # More importantly, the spacing should make a difference
    # In the fixed version, these should be different sets of positions
    # In the buggy version, they would be the same
    assert unique_positions_with_spacing != unique_positions_no_spacing, \
        "wspace and hspace parameters are not being applied when layout_engine is None"


def test_subfigures_wspace_hspace_zero_vs_none():
    """Test that wspace=0 and wspace=None behave consistently when layout_engine is None."""
    # Create a figure without a layout engine
    fig = plt.figure(figsize=(10, 10))
    fig.set_layout_engine(None)
    
    # Create subfigures with wspace=0
    subfigs_zero = fig.subfigures(2, 2, wspace=0, hspace=0)
    
    # Create subfigures with wspace=None (should default to 0 in this case)
    fig2 = plt.figure(figsize=(10, 10))
    fig2.set_layout_engine(None)
    subfigs_none = fig2.subfigures(2, 2, wspace=None, hspace=None)
    
    # Get the bounding boxes
    bboxes_zero = []
    bboxes_none = []
    
    for row in subfigs_zero:
        for subfig in row:
            bboxes_zero.append(subfig.get_window_extent())
    
    for row in subfigs_none:
        for subfig in row:
            bboxes_none.append(subfig.get_window_extent())
    
    # Both should produce the same result (tight packing)
    positions_zero = [(bbox.x0, bbox.y0, bbox.x1, bbox.y1) for bbox in bboxes_zero]
    positions_none = [(bbox.x0, bbox.y0, bbox.x1, bbox.y1) for bbox in bboxes_none]
    
    # They should be the same (both should be tight packing)
    assert len(positions_zero) == 4
    assert len(positions_none) == 4
    
    # They should produce identical results
    assert set(positions_zero) == set(positions_none), "wspace=0 and wspace=None should behave identically when layout_engine is None"


def test_subfigures_wspace_hspace_constrained_layout():
    """Test that wspace and hspace work with constrained layout (should work in both cases)."""
    # Create a figure with constrained layout engine
    fig = plt.figure(figsize=(10, 10))
    fig.set_layout_engine('constrained')
    
    # Create subfigures with wspace and hspace
    subfigs = fig.subfigures(2, 2, wspace=0.2, hspace=0.3)
    
    # Get the bounding boxes
    bboxes = []
    for row in subfigs:
        for subfig in row:
            bboxes.append(subfig.get_window_extent())
    
    # Should have 4 subfigures
    assert len(bboxes) == 4
    
    # Positions should be different from tight packing
    positions = [(bbox.x0, bbox.y0, bbox.x1, bbox.y1) for bbox in bboxes]
    unique_positions = set(positions)
    
    # Should have multiple positions due to spacing
    assert len(unique_positions) > 1, "With constrained layout, wspace/hspace should create different positions"