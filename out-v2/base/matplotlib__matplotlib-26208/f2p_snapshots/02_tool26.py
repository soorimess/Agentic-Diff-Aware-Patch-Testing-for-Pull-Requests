import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_preserves_datalim():
    """
    Test that twinx() does not corrupt data limits when stackplot is used on the original axis.
    
    This is a regression test for the bug where data limits get replaced by inf 
    for charts with twinx if ax1 is a stackplot.
    
    Before the fix: ax1.dataLim becomes [inf, -inf] after calling twinx()
    After the fix: ax1.dataLim should remain unchanged
    """
    # Test data from the bug report
    df1_index = ['16 May', '17 May']
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    # Plot stackplot on the first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits for ax1
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis - this is where the bug occurs
    ax2 = ax1.twinx()
    
    # Get data limits after twinx() - this should not corrupt ax1
    ax1_datalim_after_twinx = ax1.dataLim.intervaly.copy()
    ax2_datalim_after_twinx = ax2.dataLim.intervaly.copy()
    
    # Plot on the second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final data limits
    final_ax1_datalim = ax1.dataLim.intervaly.copy()
    final_ax2_datalim = ax2.dataLim.intervaly.copy()
    
    # Verify that ax1's dataLim was not corrupted by twinx()
    # The bug manifests as ax1.dataLim becoming [inf, -inf] 
    assert not np.isinf(initial_ax1_datalim).any(), (
        f"Initial ax1 dataLim should not contain inf: {initial_ax1_datalim}"
    )
    
    # This is the key assertion - ax1's datalim should be preserved after twinx()
    assert not np.isinf(ax1_datalim_after_twinx).any(), (
        f"ax1 dataLim should not be corrupted by twinx(): {ax1_datalim_after_twinx}"
    )
    
    # The data limits should be preserved
    np.testing.assert_array_almost_equal(initial_ax1_datalim, ax1_datalim_after_twinx)
    np.testing.assert_array_almost_equal(initial_ax1_datalim, final_ax1_datalim)
    
    plt.close(fig)


def test_twiny_stackplot_preserves_datalim():
    """
    Test that twiny() does not corrupt data limits when stackplot is used on the original axis.
    
    This tests the same issue but with twiny instead of twinx.
    """
    # Test data from the bug report
    df1_index = ['16 May', '17 May']
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    # Plot stackplot on the first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits for ax1
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis - this is where the bug occurs
    ax2 = ax1.twiny()
    
    # Get data limits after twiny() - this should not corrupt ax1
    ax1_datalim_after_twiny = ax1.dataLim.intervaly.copy()
    ax2_datalim_after_twiny = ax2.dataLim.intervaly.copy()
    
    # Plot on the second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final data limits
    final_ax1_datalim = ax1.dataLim.intervaly.copy()
    final_ax2_datalim = ax2.dataLim.intervaly.copy()
    
    # Verify that ax1's dataLim was not corrupted by twiny()
    assert not np.isinf(initial_ax1_datalim).any(), (
        f"Initial ax1 dataLim should not contain inf: {initial_ax1_datalim}"
    )
    
    # This is the key assertion - ax1's datalim should be preserved after twiny()
    assert not np.isinf(ax1_datalim_after_twiny).any(), (
        f"ax1 dataLim should not be corrupted by twiny(): {ax1_datalim_after_twiny}"
    )
    
    # The data limits should be preserved
    np.testing.assert_array_almost_equal(initial_ax1_datalim, ax1_datalim_after_twiny)
    np.testing.assert_array_almost_equal(initial_ax1_datalim, final_ax1_datalim)
    
    plt.close(fig)


def test_twinx_vs_twiny_order_independence():
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
    test_twinx_stackplot_preserves_datalim()
    test_twiny_stackplot_preserves_datalim()
    test_twinx_vs_twiny_order_independence()
    print("All tests passed!")