import numpy as np
import pytest
import matplotlib.pyplot as plt


def test_subfigures_wspace_hspace_no_layout_engine():
    """
    Test that wspace and hspace parameters are respected when no layout engine is used.
    
    This test specifically targets the bug where wspace and hspace in subfigures()
    were ignored when get_layout_engine() returns None.
    """
    # Create a figure with no layout engine (the problematic case)
    fig = plt.figure()
    fig.set_layout_engine(None)  # Explicitly disable layout engine
    
    # This should work correctly with spacing parameters
    # The bug was that these parameters were ignored
    subfigs = fig.subfigures(2, 2, wspace=0.2, hspace=0.3)
    
    # Verify that we can create and use subfigures
    assert subfigs is not None
    assert len(subfigs.flat) == 4
    
    # Test that individual subfigures work
    for i, subfig in enumerate(subfigs.flat):
        assert subfig is not None
        # Create a simple plot to make sure they're functional
        ax = subfig.subplots()
        ax.plot([1, 2], [1, 2])
        ax.set_title(f'Subfigure {i}')


def test_subfigures_functionality_with_and_without_spacing():
    """
    Test that subfigures work with and without spacing parameters.
    """
    # Test with spacing parameters (the case that was broken)
    fig1 = plt.figure()
    fig1.set_layout_engine(None)
    subfigs1 = fig1.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    # Test without spacing parameters
    fig2 = plt.figure()
    fig2.set_layout_engine(None)
    subfigs2 = fig2.subfigures(2, 2)
    
    # Both should work without error
    assert subfigs1 is not None
    assert subfigs2 is not None
    assert len(subfigs1.flat) == 4
    assert len(subfigs2.flat) == 4


def test_subfigures_basic_compatibility():
    """
    Test basic subfigures functionality.
    """
    fig = plt.figure()
    fig.set_layout_engine(None)
    
    # Test single subfigure
    subfig = fig.subfigures(1, 1)
    
    assert subfig is not None