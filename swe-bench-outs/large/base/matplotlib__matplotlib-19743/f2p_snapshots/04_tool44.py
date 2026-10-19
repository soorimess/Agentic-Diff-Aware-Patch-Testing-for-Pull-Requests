"""
Test for constrained_layout support for figure.legend

This test verifies that figure.legend works properly with constrained_layout
when using "outside" location specifications.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pytest


def test_figure_legend_outside_locations_with_constrained_layout():
    """Test that figure.legend with 'outside' locations works with constrained_layout."""
    
    # Create a figure with constrained layout
    fig, axs = plt.subplots(1, 2, layout='constrained')
    
    # Add some data to the axes
    x = np.arange(0.0, 2.0, 0.02)
    y1 = np.sin(2 * np.pi * x)
    y2 = np.exp(-x)
    l1, = axs[0].plot(x, y1)
    l2, = axs[0].plot(x, y2, marker='o')

    y3 = np.sin(4 * np.pi * x)
    y4 = np.exp(-2 * x)
    l3, = axs[1].plot(x, y3, color='tab:green')
    l4, = axs[1].plot(x, y4, color='tab:red', marker='^')

    # Test different outside locations - this should work with constrained_layout
    # Test 1: outside upper right
    legend1 = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='outside upper right')
    
    # Test 2: outside right upper (different order)
    legend2 = fig.legend((l3, l4), ('Line 3', 'Line 4'), loc='outside right upper')
    
    # Verify the legends were created successfully
    assert len(fig.legends) == 2
    assert legend1 is not None
    assert legend2 is not None
    
    # Test that the outside location is properly set
    assert hasattr(legend1, '_outside_loc')
    assert hasattr(legend2, '_outside_loc')
    # The _outside_loc should be set to the primary direction
    assert legend1._outside_loc is not None
    assert legend2._outside_loc is not None
    
    plt.close(fig)


def test_figure_legend_outside_locations_axes_validation():
    """Test that 'outside' locations are only allowed for figure legends, not axes legends."""
    
    # Create a figure with axes
    fig, ax = plt.subplots()
    
    # Try to create an axes legend with outside location - should raise an error
    with pytest.raises(ValueError, match="'outside' option for loc='outside upper right' keyword argument only works for figure legends"):
        ax.legend(loc='outside upper right')
    
    # Try to create a figure legend with outside location - should work
    fig.legend(loc='outside upper right')
    
    plt.close(fig)


def test_figure_legend_basic_outside_functionality():
    """Test basic outside legend functionality."""
    
    # Create a figure with constrained layout
    fig, ax = plt.subplots(layout='constrained')
    
    # Add some data
    ax.plot([1, 2, 3], label="test1")
    ax.plot([3, 2, 1], label="test2")
    
    # Test outside upper right - this should work now
    legend = fig.legend(loc='outside upper right', title='Test Legend')
    assert legend is not None
    assert hasattr(legend, '_outside_loc')
    assert legend._outside_loc is not None
    
    plt.close(fig)


def test_figure_legend_constrained_layout_integration():
    """Test that constrained_layout properly handles figure legends with outside locations."""
    
    # Create a figure with constrained layout
    fig, ax = plt.subplots(layout='constrained')
    
    # Add some data
    ax.plot([1, 2, 3], label="test1")
    ax.plot([3, 2, 1], label="test2")
    
    # Create a legend with outside location - this should trigger the constrained_layout logic
    legend = fig.legend(loc='outside right upper')
    
    # Verify it was created successfully
    assert legend is not None
    assert len(fig.legends) == 1
    assert hasattr(legend, '_outside_loc')
    assert legend._outside_loc is not None
    
    # Test with different outside locations to ensure comprehensive coverage
    fig2, ax2 = plt.subplots(layout='constrained')
    ax2.plot([1, 2, 3], label="test1")
    ax2.plot([3, 2, 1], label="test2")
    
    # Test various outside locations to make sure they all work
    locations = ['outside upper left', 'outside lower right', 'outside left upper']
    for loc in locations:
        legend = fig2.legend(loc=loc)
        assert legend is not None
        assert hasattr(legend, '_outside_loc')
        assert legend._outside_loc is not None
    
    plt.close(fig)
    plt.close(fig2)


def test_figure_legend_outside_location_parsing():
    """Test that the parsing of outside locations works correctly."""
    
    # Test the specific logic for parsing outside locations
    fig, ax = plt.subplots(layout='constrained')
    ax.plot([1, 2, 3], label="test")
    
    # Test that the parsing logic works for different combinations
    test_cases = [
        'outside upper right',
        'outside right upper', 
        'outside upper left',
        'outside left upper',
        'outside lower right',
        'outside right lower',
        'outside lower left',
        'outside left lower'
    ]
    
    for loc in test_cases:
        legend = fig.legend(loc=loc)
        assert legend is not None
        assert hasattr(legend, '_outside_loc')
        # The _outside_loc should be set to one of the primary directions
        assert legend._outside_loc in ['upper', 'lower', 'left', 'right', 'center']
    
    plt.close(fig)


if __name__ == "__main__":
    test_figure_legend_outside_locations_with_constrained_layout()
    test_figure_legend_outside_locations_axes_validation()
    test_figure_legend_basic_outside_functionality()
    test_figure_legend_constrained_layout_integration()
    test_figure_legend_outside_location_parsing()
    print("All tests passed!")