import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_datalim_issue():
    """Test that demonstrates the bug where twinx changes dataLims for stackplot."""
    
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
    
    # Get dataLims after twinx
    datalim_ax1_after_twinx = ax1.dataLim.intervaly
    datalim_ax2_after_twinx = ax2.dataLim.intervaly
    
    # Plot on second axis
    ax2.plot(df1_index, df2_values)
    
    # Get dataLims after plotting on second axis
    datalim_ax1_after_plot = ax1.dataLim.intervaly
    datalim_ax2_after_plot = ax2.dataLim.intervaly
    
    # Close the figure to clean up
    plt.close(fig)
    
    # The bug: ax1.dataLim should not change after twinx and plot
    # But it gets changed to inf values in the buggy version
    assert not np.any(np.isinf(initial_datalim_ax1)), "Initial ax1 datalim should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_after_twinx)), "ax1 datalim after twinx should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_after_plot)), "ax1 datalim after plot should not contain inf"
    
    # The specific assertion that would catch the bug:
    # Before the fix, ax1.dataLim.intervaly would become [inf, -inf] after the twinx call
    # After the fix, it should remain the same as initial
    expected_ax1_datalim = initial_datalim_ax1
    actual_ax1_datalim = datalim_ax1_after_plot
    
    # This assertion should pass after the fix, fail before the fix
    np.testing.assert_array_equal(actual_ax1_datalim, expected_ax1_datalim)


def test_twinx_stackplot_datalim_with_plot_order():
    """Test that shows the difference in behavior when plot order is swapped."""
    
    # Set up the test case from the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Test case 1: plot on ax1 first, then stackplot on ax2 (the problematic case)
    fig1, ax1 = plt.subplots()
    ax1.plot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.stackplot(df1_index, df2_values)  # stackplot on ax2
    datalim_ax1_case1 = ax1.dataLim.intervaly
    plt.close(fig1)
    
    # Test case 2: stackplot on ax1 first, then plot on ax2 (this works correctly)
    fig2, ax1 = plt.subplots()
    ax1.stackplot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.plot(df1_index, df2_values)  # plot on ax2
    datalim_ax1_case2 = ax1.dataLim.intervaly
    plt.close(fig2)
    
    # Both cases should preserve ax1's dataLim
    assert not np.any(np.isinf(datalim_ax1_case1)), "Case 1: ax1 datalim should not contain inf"
    assert not np.any(np.isinf(datalim_ax1_case2)), "Case 2: ax1 datalim should not contain inf"
    
    # The key difference: in case 1, the bug manifests
    # The first case should behave the same as the second
    np.testing.assert_array_equal(datalim_ax1_case1, datalim_ax1_case2)


if __name__ == "__main__":
    test_twinx_stackplot_datalim_issue()
    test_twinx_stackplot_datalim_with_plot_order()
    print("All tests passed!")