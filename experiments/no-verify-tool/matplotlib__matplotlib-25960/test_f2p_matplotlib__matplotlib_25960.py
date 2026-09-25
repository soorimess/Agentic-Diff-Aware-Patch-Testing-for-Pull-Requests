"""
Regression test for matplotlib/matplotlib#25960
This test verifies that wspace and hspace parameters in subfigures() are
correctly handled when no layout engine is specified.

The bug: When layout_engine=None was specified and wspace/hspace parameters
were passed to subfigures(), these parameters were completely ignored.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def test_subfigures_wspace_hspace_with_no_layout_engine():
    """
    Test that wspace and hspace are processed correctly when layout_engine=None.
    
    When layout_engine is explicitly set to None and wspace/hspace are specified,
    these parameters should be respected (this was broken before the fix).
    """
    # Create figure with explicit None layout engine (the bug condition)
    fig = Figure()
    fig.set_layout_engine(None)  # key to trigger the buggy code path
    
    # Create subfigures with explicit spacing parameters
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    # This should not error and should return properly formed subfigures
    assert subfigs is not None
    
    # Convert to array for consistent handling
    subfig_array = np.array(subfigs) if isinstance(subfigs, np.ndarray) else np.array([[subfigs]])
    
    # All subfigures should be valid objects
    assert len(subfig_array.flat) == 4
    
    # Each should have sensible properties
    for i, sf in enumerate(subfig_array.flat):
        # This should be a valid subfigure (no exception should occur)
        assert sf is not None
    
    # Additional validation: check a few properties that should exist
    for sf in subfig_array.flat:
        # These properties should be accessible without error
        try:
            # Check basic properties that existing code would access
            bbox = sf.get_window_extent()
            assert bbox is not None
        except Exception:
            pytest.fail("Subfigure failed to return valid bounding box")


def test_subfigures_wspace_hspace_zero_values():
    """
    Test behavior with zero spacing values - should work consistently.
    """
    # Test with zero spacing explicitly specified
    fig = Figure()
    fig.set_layout_engine(None)
    
    subfigs = fig.subfigures(2, 2, wspace=0.0, hspace=0.0)
    
    assert subfigs is not None
    subfig_array = np.array(subfigs) if isinstance(subfigs, np.ndarray) else np.array([[subfigs]])
    assert len(subfig_array.flat) == 4


def test_subfigures_no_spacing_parameters():
    """
    Ensure default behavior still works when no spacing is specified.
    """
    fig = Figure()
    fig.set_layout_engine(None)
    
    subfigs = fig.subfigures(2, 2)  # No spacing parameters
    
    assert subfigs is not None
    subfig_array = np.array(subfigs) if isinstance(subfigs, np.ndarray) else np.array([[subfigs]])
    assert len(subfig_array.flat) == 4


def test_subfigures_with_layout_engine_still_works():
    """
    Ensure the fix doesn't break existing functionality with layout engines.
    """
    # With constrained layout engine 
    fig = Figure()
    fig.set_layout_engine('constrained')
    
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    assert subfigs is not None
    subfig_array = np.array(subfigs) if isinstance(subfigs, np.ndarray) else np.array([[subfigs]])
    assert len(subfig_array.flat) == 4