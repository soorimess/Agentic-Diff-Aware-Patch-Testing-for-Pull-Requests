"""
Regression tests for the subfigures wspace/hspace bug.

Before the fix, wspace and hspace parameters in Figure.subfigures
would be ignored when not using a layout engine (e.g., constrained layout).
This test verifies that these parameters are properly respected.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.transforms import Bbox


def test_subfigures_wspace_hspace_respected_when_no_layout_engine():
    """
    Test that wspace and hspace parameters are actually applied to subfigure positioning
    when no layout engine is active (the condition that causes the bug).
    
    When layout_engine is None and spacing is specified, 
    spacing parameters should actually matter for positioning.
    """
    # Create a figure without layout engine (triggers bug condition)
    fig = Figure(figsize=(10, 8))
    
    # Create subfigures with different spacing parameters 
    subfigs_no_space = fig.subfigures(2, 2, wspace=0.0, hspace=0.0)
    subfigs_with_space = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    # Get positions of corresponding subfigures (e.g., second subfigure in each)
    bbox_no_space = [sf.get_tightbbox(fig) for sf in subfigs_no_space.flat]
    bbox_with_space = [sf.get_tightbbox(fig) for sf in subfigs_with_space.flat]
    
    # Must have at least 2 subfigures for comparison
    assert len(bbox_no_space) >= 2 and len(bbox_with_space) >= 2
    
    # Compare positions - the second subfigures should be positioned differently
    pos_no_space = bbox_no_space[1]
    pos_with_space = bbox_with_space[1]
    
    # Calculate differences in positioning
    diff_x = abs(pos_no_space.x0 - pos_with_space.x0)
    diff_y = abs(pos_no_space.y0 - pos_with_space.y0)
    
    # If spacing works correctly, the positions should differ
    # This should hold after the fix, fail before the fix
    assert diff_x > 0.001 or diff_y > 0.001, (
        "wspace/hspace parameters are not being applied to subfigure positioning. "
        "When layout_engine is None, spacing should make a visible difference."
    )


def test_subfigures_default_behavior_works():
    """
    Test that the basic subfigures functionality works correctly.
    """
    fig = Figure(figsize=(10, 8))
    
    # Should work without errors
    subfigs = fig.subfigures(2, 2, wspace=None, hspace=None)
    
    assert subfigs.shape == (2, 2)
    assert len(subfigs.flat) == 4
    assert subfigs[0, 0] is not None
    assert subfigs[1, 1] is not None


def test_subfigures_original_bug_reproduction():
    """
    Test exact reproduction of bug report scenario.
    
    Original bug: figs = plt.figure().subfigures(2, 2, wspace=0, hspace=0)
    This should work without error and with spacing respected.
    """
    fig = Figure(figsize=(10, 8))
    
    # The bug reported was that when spacing was non-zero, it didn't work
    # This tests that spacing can work 
    figs_zero = fig.subfigures(2, 2, wspace=0, hspace=0)
    figs_nonzero = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)  # This was the failing case
    
    # Basic functionality check - no exceptions
    assert len(figs_zero.flat) == 4
    assert len(figs_nonzero.flat) == 4
    
    # Test that we can create plots on them
    for fig_sub in figs_zero.flat:
        ax = fig_sub.subplots()
        ax.plot([1, 2], [3, 4])
    
    for fig_sub in figs_nonzero.flat:
        ax = fig_sub.subplots()  
        ax.plot([1, 2], [3, 4])


def test_subfigures_with_explicit_none_spacing():
    """
    Test behavior when explicit None values are provided.
    """
    fig = Figure(figsize=(10, 8))
    
    # Explicit None parameters should work  
    subfigs = fig.subfigures(2, 2, wspace=None, hspace=None)
    
    assert subfigs.shape == (2, 2)
    
    # Should be able to create plots
    for sf in subfigs.flat:
        ax = sf.subplots()
        ax.plot([1, 2], [3, 4])