"""
Test for constrained_layout support for figure.legend

This test verifies that figure.legend works with constrained_layout
by testing the 'outside' location options.
"""
import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_figure_legend_outside_locations():
    """Test that figure.legend works with 'outside' locations in constrained_layout."""
    # Create a figure with constrained layout
    fig, axs = plt.subplots(1, 2, layout='constrained')
    
    # Create some sample data
    x = np.arange(0.0, 2.0, 0.02)
    y1 = np.sin(2 * np.pi * x)
    y2 = np.exp(-x)
    l1, = axs[0].plot(x, y1)
    l2, = axs[0].plot(x, y2, marker='o')

    y3 = np.sin(4 * np.pi * x)
    y4 = np.exp(-2 * x)
    l3, = axs[1].plot(x, y3, color='tab:green')
    l4, = axs[1].plot(x, y4, color='tab:red', marker='^')

    # This should work without error in the fixed version
    # The main point is that it doesn't raise ValueError about invalid loc
    try:
        legend1 = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='upper left')
        legend2 = fig.legend((l3, l4), ('Line 3', 'Line 4'), loc='outside right upper')
        # If we get here without exception, the test passes
        assert legend1 is not None
        assert legend2 is not None
    except ValueError as e:
        if 'outside' in str(e) and 'valid' in str(e):
            # This is the expected error before the fix
            pytest.fail("figure.legend with 'outside' location failed - this should work after the fix")
        else:
            raise  # Re-raise if it's a different error
    
    plt.close(fig)


def test_axes_legend_outside_still_errors():
    """Test that axes.legend still raises an error for outside locations."""
    fig, ax = plt.subplots()
    
    # Create some sample data
    line, = ax.plot([1, 2], [1, 2], label='TEST')
    
    # This should still raise an error because outside locations are only for figure legends
    with pytest.raises(ValueError) as exc_info:
        ax.legend(loc='outside upper right')
    
    # The error message should mention the restriction
    error_msg = str(exc_info.value)
    assert 'outside' in error_msg.lower()
    assert 'figure' in error_msg.lower()
    
    plt.close(fig)


def test_various_outside_locations():
    """Test that various outside location formats work for figure legends."""
    # Create a figure with constrained layout
    fig, ax = plt.subplots(figsize=(6, 4), layout='constrained')
    
    # Create some sample data
    ax.plot([1, 2], [1, 2], label='TEST')
    
    # Test different outside locations - these should all work in the fixed version
    locations = [
        'outside upper left',
        'outside upper center', 
        'outside upper right',
        'outside lower left',
        'outside lower center',
        'outside lower right',
        'outside left upper',
        'outside right upper',
        'outside left lower',
        'outside right lower'
    ]
    
    # All of these should work without raising ValueError about invalid loc
    for loc in locations:
        try:
            legend = fig.legend(loc=loc, title=loc)
            assert legend is not None
        except ValueError as e:
            if 'outside' in str(e) and 'valid' in str(e):
                pytest.fail(f"figure.legend with 'outside' location '{loc}' failed - this should work after the fix")
            else:
                raise
    
    plt.close(fig)


if __name__ == "__main__":
    test_figure_legend_outside_locations()
    test_axes_legend_outside_still_errors()
    test_various_outside_locations()
    print("All tests passed!")