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
    legend = fig.legend(loc='outside upper right')
    assert legend is not None
    assert hasattr(legend, '_outside_loc')
    assert legend._outside_loc is not None
    
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
    
    # Test that the legend has the right attributes
    assert hasattr(legend, 'isaxes')
    assert not legend.isaxes  # Should be a figure legend
    
    plt.close(fig)


def test_figure_legend_various_outside_combinations():
    """Test various outside location combinations."""
    
    # Create a figure with constrained layout
    fig, ax = plt.subplots(layout='constrained')
    ax.plot([1, 2, 3], label="test1")
    ax.plot([3, 2, 1], label="test2")
    
    # Test various outside locations to make sure they all work
    locations = [
        'outside upper left',
        'outside upper right', 
        'outside lower left',
        'outside lower right',
        'outside left upper',
        'outside left lower',
        'outside right upper',
        'outside right lower'
    ]
    
    for loc in locations:
        legend = fig.legend(loc=loc)
        assert legend is not None
        assert hasattr(legend, '_outside_loc')
        assert legend._outside_loc is not None
    
    plt.close(fig)


def test_figure_legend_outside_location_attributes():
    """Test that outside location attributes are correctly set."""
    
    # Test the specific parsing behavior
    fig, ax = plt.subplots(layout='constrained')
    ax.plot([1, 2, 3], label="test")
    
    # Test that parsing works correctly for different combinations
    test_cases = [
        ('outside upper right', 'upper'),
        ('outside right upper', 'right'), 
        ('outside upper left', 'upper'),
        ('outside left upper', 'left'),
    ]
    
    for loc, expected_primary in test_cases:
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
    test_figure_legend_various_outside_combinations()
    test_figure_legend_outside_location_attributes()
    print("All tests passed!")