"""
Regression test for matplotlib bug where wspace and hspace in subfigures 
were not working when no layout engine was used.

This test verifies that when wspace and hspace parameters are provided to 
Figure.subfigures() and no layout engine is used, they actually affect the 
spacing between subfigures.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import pytest


def test_subfigures_wspace_hspace_no_layout_engine():
    """
    Test that wspace and hspace parameters are respected when no layout engine is used.
    
    Before the fix, wspace and hspace were ignored when no layout engine was used.
    After the fix, they should properly space the subfigures.
    """
    # Create a figure with no layout engine (default behavior)
    fig = plt.figure()
    fig.set_layout_engine(None)  # Explicitly set to None to ensure no layout engine
    
    # Create subfigures with explicit wspace and hspace
    subfigs = fig.subfigures(2, 2, wspace=0.2, hspace=0.2)
    
    # Get the bounding boxes of the subfigures to check spacing
    # We'll check the positions to see if spacing was applied
    
    # Get the actual positions of subfigures
    # The key test is that with wspace=0.2, there should be visible spacing
    bbox1 = subfigs[0, 0].get_window_extent()
    bbox2 = subfigs[0, 1].get_window_extent()  # Right neighbor
    bbox3 = subfigs[1, 0].get_window_extent()  # Bottom neighbor
    
    # Before the fix: wspace/hspace were ignored, so subfigures would be right next to each other
    # After the fix: wspace/hspace should create actual spacing
    
    # Check that there is actual horizontal spacing (x1 of first should be < x0 of second)
    # If the bug exists, they would be equal (no spacing)
    if bbox1.x1 == bbox2.x0:
        # This indicates the bug - no spacing was applied
        pytest.fail("wspace parameter not working - subfigures are not spaced horizontally")
    
    # Check that there is actual vertical spacing
    if bbox1.y1 == bbox3.y0:
        # This indicates the bug - no spacing was applied
        pytest.fail("hspace parameter not working - subfigures are not spaced vertically")


def test_subfigures_wspace_hspace_with_constrained_layout():
    """
    Test that wspace and hspace parameters work correctly with constrained layout.
    
    This ensures that the behavior with constrained layout is not broken.
    """
    # Create a figure with constrained layout engine
    fig = plt.figure()
    fig.set_layout_engine('constrained')
    
    # Create subfigures with explicit wspace and hspace
    subfigs = fig.subfigures(2, 2, wspace=0.2, hspace=0.2)
    
    # Get the bounding boxes
    bbox1 = subfigs[0, 0].get_window_extent()
    bbox2 = subfigs[0, 1].get_window_extent()
    bbox3 = subfigs[1, 0].get_window_extent()
    
    # With constrained layout, spacing should also be applied
    # Check that there is actual horizontal spacing
    if bbox1.x1 == bbox2.x0:
        pytest.fail("wspace parameter not working with constrained layout - subfigures are not spaced horizontally")
    
    # Check that there is actual vertical spacing
    if bbox1.y1 == bbox3.y0:
        pytest.fail("hspace parameter not working with constrained layout - subfigures are not spaced vertically")


def test_subfigures_no_spacing_parameters():
    """
    Test that when no spacing parameters are provided, behavior is unchanged.
    """
    # Create a figure with no layout engine
    fig = plt.figure()
    fig.set_layout_engine(None)
    
    # Create subfigures without explicit wspace and hspace (should use defaults)
    subfigs = fig.subfigures(2, 2)
    
    # Basic functionality should still work
    assert subfigs.shape == (2, 2)
    assert len(subfigs.flat) == 4


def test_subfigures_zero_spacing():
    """
    Test that zero spacing parameters work correctly.
    """
    # Create a figure with no layout engine
    fig = plt.figure()
    fig.set_layout_engine(None)
    
    # Create subfigures with zero spacing
    subfigs = fig.subfigures(2, 2, wspace=0, hspace=0)
    
    # This should work without error and create subfigures with no spacing
    assert subfigs.shape == (2, 2)
    assert len(subfigs.flat) == 4


if __name__ == "__main__":
    # Run the tests manually for debugging
    try:
        test_subfigures_wspace_hspace_no_layout_engine()
        print("test_subfigures_wspace_hspace_no_layout_engine: PASSED")
    except Exception as e:
        print(f"test_subfigures_wspace_hspace_no_layout_engine: FAILED - {e}")
        
    try:
        test_subfigures_wspace_hspace_with_constrained_layout()
        print("test_subfigures_wspace_hspace_with_constrained_layout: PASSED")
    except Exception as e:
        print(f"test_subfigures_wspace_hspace_with_constrained_layout: FAILED - {e}")
        
    try:
        test_subfigures_no_spacing_parameters()
        print("test_subfigures_no_spacing_parameters: PASSED")
    except Exception as e:
        print(f"test_subfigures_no_spacing_parameters: FAILED - {e}")
        
    try:
        test_subfigures_zero_spacing()
        print("test_subfigures_zero_spacing: PASSED")
    except Exception as e:
        print(f"test_subfigures_zero_spacing: FAILED - {e}")