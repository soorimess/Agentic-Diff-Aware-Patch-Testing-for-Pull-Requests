import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_datalim_preservation():
    """
    Test that twinx does not corrupt dataLims when using stackplot.
    
    This test reproduces the bug where dataLims of the first axis get 
    replaced by inf for charts with twinx if ax1 is a stackplot.
    """
    
    # Set up the test case from the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Create figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial dataLim for ax1
    initial_datalim_ax1 = ax1.dataLim.intervaly
    
    # Create second axis with twinx
    ax2 = ax1.twinx()
    
    # Get dataLims after twinx (this is where the bug occurs)
    datalim_ax1_after_twinx = ax1.dataLim.intervaly
    datalim_ax2_after_twinx = ax2.dataLim.intervaly
    
    # Plot on second axis
    ax2.plot(df1_index, df2_values)
    
    # Get dataLims after plotting on second axis
    datalim_ax1_after_plot = ax1.dataLim.intervaly
    datalim_ax2_after_plot = ax2.dataLim.intervaly
    
    # Close the figure to clean up
    plt.close(fig)
    
    # The bug manifests as ax1.dataLim.intervaly becoming [inf, -inf] 
    # after the twinx() call, which should not happen
    assert not np.any(np.isinf(initial_datalim_ax1)), "Initial ax1 datalim should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_after_twinx)), "ax1 datalim after twinx should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_after_plot)), "ax1 datalim after plot should not contain inf"
    
    # The key assertion: ax1's dataLim should be preserved after twinx
    # The bug makes it [inf, -inf] instead of the original values
    np.testing.assert_array_equal(datalim_ax1_after_plot, initial_datalim_ax1,
                                  "ax1 dataLim should be preserved after twinx and plot")


def test_twinx_stackplot_order_independence():
    """
    Test that the order of operations doesn't affect dataLim preservation.
    
    The bug was specifically with stackplot on ax1 and then twinx/plot on ax2.
    This test ensures the fix works regardless of operation order.
    """
    
    # Set up the test case from the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Test case 1: stackplot on ax1, then twinx, then plot on ax2 (the problematic case)
    fig1, ax1 = plt.subplots()
    ax1.stackplot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.plot(df1_index, df2_values)  # plot on ax2
    datalim_ax1_case1 = ax1.dataLim.intervaly
    plt.close(fig1)
    
    # Test case 2: plot on ax1, then twinx, then stackplot on ax2 (this worked before)
    fig2, ax1 = plt.subplots()
    ax1.plot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.stackplot(df1_index, df2_values)  # stackplot on ax2
    datalim_ax1_case2 = ax1.dataLim.intervaly
    plt.close(fig2)
    
    # Both cases should preserve ax1's dataLim correctly
    assert not np.any(np.isinf(datalim_ax1_case1)), "Case 1: ax1 datalim should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_case2)), "Case 2: ax1 datalim should not contain inf"
    
    # Both should behave the same way (the fix should make them consistent)
    np.testing.assert_array_equal(datalim_ax1_case1, datalim_ax1_case2,
                                  "Both operation orders should preserve ax1 dataLim consistently")


if __name__ == "__main__":
    test_twinx_stackplot_datalim_preservation()
    test_twinx_stackplot_order_independence()
    print("All tests passed!")