import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_datalim_issue():
    """
    Test for bug where data limits get replaced by inf for charts with twinx 
    if ax1 is a stackplot.
    
    This reproduces the issue described in the bug report where:
    - When using twin x-axis (two-y-axis charts)
    - The data limits (dataLims) of the first axis (ax1) get changed to ±inf 
    - When plotting a stackplot on the second axis (ax2)
    """
    
    def print_datalim(*ax):
        """Helper to print data limits"""
        for ax_ in ax:
            print(ax_.dataLim.intervaly, end=' / ')
        print()

    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    # This should not affect ax1's dataLim
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits for ax1
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    print("After stackplot on ax1:")
    print_datalim(ax1)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    print("After twinx:")
    print_datalim(ax1, ax2)

    # This should not change ax1's dataLim
    ax2.plot(df1_index, df2_values)
    print("After plot on ax2:")
    print_datalim(ax1, ax2)
    
    # Check that ax1's dataLim hasn't been corrupted
    final_ax1_datalim = ax1.dataLim.intervaly.copy()
    
    # The bug manifests as ax1.dataLim becoming [inf, -inf] or similar
    # We expect ax1's dataLim to remain the same as before ax2 was created
    assert not np.isinf(initial_ax1_datalim).any(), (
        f"Initial ax1 dataLim should not contain inf: {initial_ax1_datalim}"
    )
    
    # Check that ax1's dataLim hasn't been corrupted by the twinx operation
    assert not np.isinf(final_ax1_datalim).any(), (
        f"Final ax1 dataLim should not contain inf: {final_ax1_datalim}"
    )
    
    # The data limits should be preserved
    np.testing.assert_array_almost_equal(initial_ax1_datalim, final_ax1_datalim)
    
    plt.close(fig)


def test_twinx_stackplot_datalim_issue_order_independence():
    """
    Test that the order of operations doesn't matter - 
    the bug should not occur regardless of which axis gets the stackplot.
    """
    
    df1_index = ['16 May', '17 May']  
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    # Test case 1: stackplot on ax1, plot on ax2 (the problematic case)
    fig1, ax1 = plt.subplots()
    ax1.stackplot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.plot(df1_index, df2_values)
    
    # Check ax1 dataLim is preserved
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    assert not np.isinf(initial_ax1_datalim).any(), (
        "ax1 dataLim should not contain inf when stackplot is on ax1"
    )
    
    plt.close(fig1)
    
    # Test case 2: plot on ax1, stackplot on ax2 (should work fine)
    fig2, ax1 = plt.subplots()
    ax1.plot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.stackplot(df1_index, df2_values)
    
    # Check ax1 dataLim is preserved
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    assert not np.isinf(initial_ax1_datalim).any(), (
        "ax1 dataLim should not contain inf when stackplot is on ax2"
    )
    
    plt.close(fig2)


if __name__ == "__main__":
    test_twinx_stackplot_datalim_issue()
    test_twinx_stackplot_datalim_issue_order_independence()
    print("All tests passed!")