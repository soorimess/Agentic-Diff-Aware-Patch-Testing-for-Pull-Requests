import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_preserves_datalim():
    """
    Test that twinx() does not corrupt data limits when stackplot is used on the original axis.
    
    This is a regression test for the bug where data limits get replaced by inf 
    for charts with twinx if ax1 is a stackplot.
    
    The bug occurs because when twinx() is called, ax2.xaxis.units = self.xaxis.units
    causes issues with data limit calculation when stackplot is used.
    """
    # Test data from the bug report
    df1_index = ['16 May', '17 May']
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    # Plot stackplot on the first axis - this is the key operation that triggers the bug
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits for ax1
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis - this is where the bug occurs
    ax2 = ax1.twinx()
    
    # Get data limits after twinx() - this should not corrupt ax1
    ax1_datalim_after_twinx = ax1.dataLim.intervaly.copy()
    
    # Plot on the second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final data limits
    final_ax1_datalim = ax1.dataLim.intervaly.copy()
    
    # Verify that ax1's dataLim was not corrupted by twinx()
    # The bug manifests as ax1.dataLim becoming [inf, -inf] 
    assert not np.isinf(initial_ax1_datalim).any(), (
        f"Initial ax1 dataLim should not contain inf: {initial_ax1_datalim}"
    )
    
    # This is the key assertion - ax1's datalim should be preserved after twinx()
    assert not np.isinf(ax1_datalim_after_twinx).any(), (
        f"ax1 dataLim should not be corrupted by twinx(): {ax1_datalim_after_twinx}"
    )
    
    # The data limits should be preserved (this is what the fix ensures)
    np.testing.assert_array_almost_equal(initial_ax1_datalim, ax1_datalim_after_twinx)
    np.testing.assert_array_almost_equal(initial_ax1_datalim, final_ax1_datalim)
    
    plt.close(fig)


def test_twinx_vs_twiny_behavior_difference():
    """
    Test that demonstrates the difference between twinx and twiny behavior.
    
    The bug specifically affects twinx, not twiny, because the fix was applied only 
    to the twinx method.
    """
    df1_index = ['16 May', '17 May']  
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    # Test case: stackplot on ax1, plot on ax2 (the problematic case with twinx)
    fig1, ax1 = plt.subplots()
    ax1.stackplot(df1_index, df1_values)
    ax2 = ax1.twinx()
    ax2.plot(df1_index, df2_values)
    
    # Check ax1 dataLim is preserved with twinx
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    assert not np.isinf(initial_ax1_datalim).any(), (
        "ax1 dataLim should not contain inf when stackplot is on ax1 with twinx"
    )
    
    plt.close(fig1)
    
    # Test case: stackplot on ax1, plot on ax2 (should work fine with twiny) 
    fig2, ax1 = plt.subplots()
    ax1.stackplot(df1_index, df1_values)
    ax2 = ax1.twiny()
    ax2.plot(df1_index, df2_values)
    
    # Check ax1 dataLim is preserved with twiny
    initial_ax1_datalim = ax1.dataLim.intervaly.copy()
    assert not np.isinf(initial_ax1_datalim).any(), (
        "ax1 dataLim should not contain inf when stackplot is on ax1 with twiny"
    )
    
    plt.close(fig2)


if __name__ == "__main__":
    test_twinx_stackplot_preserves_datalim()
    test_twinx_vs_twiny_behavior_difference()
    print("All tests passed!")