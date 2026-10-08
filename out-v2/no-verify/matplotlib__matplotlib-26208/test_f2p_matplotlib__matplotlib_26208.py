"""
Regression test for matplotlib issue where data limits get replaced by inf
for charts with twinx if ax1 is a stackplot.

This test ensures that when using twinx() with a stackplot on the first axis,
the data limits of the first axis remain unchanged after plotting on the second axis.
"""

import matplotlib.pyplot as plt
import numpy as np


def test_twinx_stackplot_datalim_preservation():
    """
    Test that data limits of the first axis are preserved when using twinx()
    with stackplot on first axis and regular plot on second axis.
    
    This is a regression test for the bug where ax1.dataLim gets changed to ±inf
    when using twinx() after stackplot on ax1.
    """
    # Setup data as in the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Create figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits of ax1
    initial_ax1_datalim = ax1.dataLim.intervaly
    
    # Create second axis with twinx
    ax2 = ax1.twinx()
    
    # Get data limits after twinx (should be unchanged)
    ax1_datalim_after_twinx = ax1.dataLim.intervaly
    ax2_datalim_after_twinx = ax2.dataLim.intervaly
    
    # Plot on second axis
    ax2.plot(df1_index, df2_values)
    
    # Get data limits after plotting on second axis
    ax1_datalim_after_plot = ax1.dataLim.intervaly
    ax2_datalim_after_plot = ax2.dataLim.intervaly
    
    # The bug: ax1.dataLim gets changed to ±inf after plotting on ax2
    # So we check that ax1's dataLim is preserved
    expected_ax1_datalim = initial_ax1_datalim
    
    # Check that ax1's dataLim hasn't changed (this is the main assertion)
    assert np.allclose(ax1_datalim_after_plot, expected_ax1_datalim), \
        f"ax1 dataLim changed from {expected_ax1_datalim} to {ax1_datalim_after_plot}"
    
    # Check that ax2's dataLim is correct
    expected_ax2_datalim = np.array([-2.983302, -0.085014])
    assert np.allclose(ax2_datalim_after_plot, expected_ax2_datalim), \
        f"ax2 dataLim incorrect: expected {expected_ax2_datalim}, got {ax2_datalim_after_plot}"
    
    # Additional check: ensure ax1 dataLim is not inf (the core bug)
    assert not np.any(np.isinf(ax1_datalim_after_plot)), \
        f"ax1 dataLim contains inf values: {ax1_datalim_after_plot}"
    
    plt.close('all')


def test_twinx_stackplot_order_independence():
    """
    Test that the order of plotting doesn't affect data limit preservation.
    This verifies that the issue is specifically with stackplot on first axis,
    not general twinx behavior.
    """
    # Setup data
    df1_index = ['16 May', '17 May']
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Test the working case: plot on ax1 first, then stackplot on ax2
    fig, ax1 = plt.subplots()
    ax1.plot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.stackplot(df1_index, df1_values)  # stackplot on second axis
    
    # Both axes should have reasonable data limits
    ax1_datalim = ax1.dataLim.intervaly
    ax2_datalim = ax2.dataLim.intervaly
    
    # Neither should be inf
    assert not np.any(np.isinf(ax1_datalim)), f"ax1 dataLim contains inf: {ax1_datalim}"
    assert not np.any(np.isinf(ax2_datalim)), f"ax2 dataLim contains inf: {ax2_datalim}"
    
    plt.close('all')


if __name__ == "__main__":
    test_twinx_stackplot_datalim_preservation()
    test_twinx_stackplot_order_independence()
    print("All tests passed!")