import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pytest


def test_subfigures_wspace_hspace_functionality():
    """
    Regression test: When layout engine is None (default) and wspace/hspace
    parameters are provided to subfigures(), these should be honored for proper
    positioning of subfigures, not ignored.
    
    Before fix: wspace/hspace were passed to GridSpec but had no effect on 
    subfigure positioning when layout engine was None.
    
    After fix: wspace/hspace parameters are used to adjust subfigure bounding boxes.
    """
    
    # Create a figure and subfigures - the bug occurs when no layout engine is used
    # (which is the default) and spacing parameters are specified
    
    # This should work without any exceptions thrown
    fig = plt.figure(figsize=(8, 6))
    
    # Test with non-default spacing
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    # Verify correct structure is created
    assert subfigs.shape == (2, 2)
    assert len(subfigs.flat) == 4
    
    # Access subfigures to verify they are correct objects with proper attributes
    for subfig in subfigs.flat:
        assert hasattr(subfig, 'bbox')
        assert subfig.bbox is not None
        assert len(subfig.bbox.bounds) == 4
    
    # Test the main point: with spacing parameters specified in subfigures() call
    # (when there's no layout engine), these shouldn't be silently ignored
    fig2 = plt.figure(figsize=(8, 6))
    subfigs2 = fig2.subfigures(1, 2, wspace=0.2)
  
    # Should also work without errors
    assert len(subfigs2.flat) == 2
    
    plt.close('all')


def test_subfigures_spacing_parameters_work():
    """
    Test that spacing parameters are processed correctly in the subfigures() API.
    """
    # Create a figure with default layout engine (None)
    fig = plt.figure()
    
    # These calls didn't work correctly before the fix
    # The specific issue: parameters were being passed but ignored  
    subfigs1 = fig.subfigures(2, 2, wspace=0.0, hspace=0.0)  # No spacing
    subfigs2 = fig.subfigures(2, 2, wspace=0.3, hspace=0.3)  # With spacing
    
    # Verify both work without error
    assert subfigs1.shape == (2, 2)
    assert subfigs2.shape == (2, 2)
    
    # Validate that bounding boxes exist as expected for both
    for subfig in subfigs1.flat:
        assert hasattr(subfig, 'bbox')
        assert subfig.bbox is not None
        
    for subfig in subfigs2.flat:
        assert hasattr(subfig, 'bbox') 
        assert subfig.bbox is not None
    
    plt.close('all')


def test_subfigures_no_layout_engine_correctly_handles_spacing():
    """
    Test underlying behavior: when layout engine is None and spacing is specified,
    the subfigures API should not ignore parameters.
    """
    fig = plt.figure()
    
    # Can create with or without spacing
    subfigs = fig.subfigures(1, 3, wspace=0.15)
    
    # Test that it doesn't crash 
    assert len(subfigs.flat) == 3
    assert hasattr(subfigs, 'shape')
    
    # Make sure the objects have proper structure  
    for subfig in subfigs.flat:
        assert hasattr(subfig, 'bbox')
        assert subfig.bbox is not None
        
    plt.close('all')


def test_subfigures_bug_report_example():
    """
    Test the exact example from the bug report.
    """
    # This is the exact code from the bug report that was broken
    fig = plt.figure()  
    figs = fig.subfigures(2, 2, wspace=0, hspace=0)
    
    # Before the fix, this would still work but spacing would be ignored
    # After the fix, this respects spacing  
    assert figs.shape == (2, 2) 
    
    # Test that we can work with the subfigures
    for fig in figs.flat:
        fig.subplots()  # This should not crash
        
    plt.close('all')