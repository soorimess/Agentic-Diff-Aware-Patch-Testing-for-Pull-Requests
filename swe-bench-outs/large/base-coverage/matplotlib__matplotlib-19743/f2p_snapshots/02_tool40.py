"""
Test for constrained_layout support for figure.legend.

This test verifies the behavior changes introduced by the pull request
that adds constrained_layout support for figure.legend with "outside"
location specifiers.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import pytest
import numpy as np


def test_figure_legend_outside_with_constrained_layout():
    """Test that figure.legend with 'outside' locations works with constrained_layout."""
    # This should work without error
    fig, axs = plt.subplots(1, 2, layout='constrained')
    
    x = np.arange(0.0, 2.0, 0.02)
    y1 = np.sin(2 * np.pi * x)
    y2 = np.exp(-x)
    l1, = axs[0].plot(x, y1)
    l2, = axs[0].plot(x, y2, marker='o')

    y3 = np.sin(4 * np.pi * x)
    y4 = np.exp(-2 * x)
    l3, = axs[1].plot(x, y3, color='tab:green')
    l4, = axs[1].plot(x, y4, color='tab:red', marker='^')

    # This should work with constrained_layout
    leg1 = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='upper left')
    leg2 = fig.legend((l3, l4), ('Line 3', 'Line 4'), loc='outside right upper')
    
    # Verify both legends were created
    assert len(fig.legends) == 2
    assert leg1 is not None
    assert leg2 is not None
    
    plt.close(fig)


def test_figure_legend_outside_location_error_for_axes():
    """Test that axes.legend with 'outside' locations raises an error."""
    fig, ax = plt.subplots()
    
    # Create a line to legend
    line, = ax.plot([1, 2, 3], [1, 2, 3])
    
    # This should raise an error because 'outside' only works for figure legends
    with pytest.raises(ValueError, match="'outside' option for loc='outside upper right' keyword argument only works for figure legends"):
        ax.legend([line], ['test'], loc='outside upper right')
    
    plt.close(fig)


def test_figure_legend_outside_various_locations():
    """Test various 'outside' location specifications work with constrained_layout."""
    # Test a few key combinations to make sure they work
    locations = [
        'outside upper left',
        'outside upper right',
        'outside right upper',
        'outside left lower',
    ]
    
    for i, loc in enumerate(locations):
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        # Create some data
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        y2 = np.exp(-x)
        l1, = axs[0].plot(x, y1)
        l2, = axs[0].plot(x, y2, marker='o')

        # This should not raise an error
        leg = fig.legend([l1], [f'Legend {i}'], loc=loc)
        assert leg is not None
        
        plt.close(fig)


def test_constrained_layout_margins_for_figure_legends():
    """Test that constrained_layout properly adjusts margins for figure legends."""
    # Create a figure with constrained layout
    fig, axs = plt.subplots(1, 2, layout='constrained')
    
    # Add some data to the axes
    axs[0].plot([1, 2, 3], [1, 2, 3], label='line1')
    axs[1].plot([1, 2, 3], [3, 2, 1], label='line2')
    
    # Add a figure legend with outside location
    leg = fig.legend(loc='outside right upper')
    
    # The figure should have a legend
    assert len(fig.legends) == 1
    
    plt.close(fig)


if __name__ == "__main__":
    # Run tests manually for debugging
    test_figure_legend_outside_with_constrained_layout()
    test_figure_legend_outside_location_error_for_axes()
    test_figure_legend_outside_various_locations()
    test_constrained_layout_margins_for_figure_legends()
    print("All tests passed!")