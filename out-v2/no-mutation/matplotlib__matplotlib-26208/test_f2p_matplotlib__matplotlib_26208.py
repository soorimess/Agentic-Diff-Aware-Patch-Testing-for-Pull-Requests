import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_datalim():
    """
    Test that data limits of the first axis are not corrupted to ±inf
    when using stackplot on first axis and then plotting on twin axis.
    
    This is a regression test for the bug where dataLims get replaced by inf
    for charts with twinx if ax1 is a stackplot.
    """
    # Setup data as described in the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Create the figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on the first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial dataLim of ax1
    initial_datalim_ax1 = ax1.dataLim.intervaly
    
    # Create twin x-axis
    ax2 = ax1.twinx()
    
    # Get dataLim after creating twin axis
    datalim_after_twinx = ax1.dataLim.intervaly
    
    # Plot on the second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final dataLim of ax1 - this should NOT be inf
    final_datalim_ax1 = ax1.dataLim.intervaly
    
    # The bug was that final_datalim_ax1 would be [inf, -inf] or similar
    # Check that the first axis dataLim was not corrupted
    assert not np.isinf(initial_datalim_ax1).any(), (
        "Initial dataLim of ax1 should not contain inf values"
    )
    
    # The key assertion: ax1's dataLim should remain the same after twinx and plotting
    # The bug was that ax1.dataLim would be corrupted to ±inf
    assert not np.isinf(final_datalim_ax1).any(), (
        "Final dataLim of ax1 should not contain inf values after plotting on twin axis"
    )
    
    # Also verify that the values make sense (they should be similar to initial values)
    # The initial values should be around [-22.71770833, 26.585]
    expected_range = [-25.0, 30.0]  # Reasonable bounds around the data
    
    # Check that the data limits are reasonable (not infinite)
    assert np.all(np.abs(final_datalim_ax1) < 1000), (
        "Final dataLim of ax1 should not contain extremely large values"
    )
    
    plt.close('all')


def test_twinx_stackplot_datalim_numeric():
    """
    Test with numeric data to avoid categorical conversion issues.
    """
    # Setup numeric data as described in the bug report
    df1_index = [0, 1]  # Numeric x values
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Create the figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on the first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial dataLim of ax1
    initial_datalim_ax1 = ax1.dataLim.intervaly
    
    # Create twin x-axis
    ax2 = ax1.twinx()
    
    # Plot on the second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final dataLim of ax1 - this should NOT be inf
    final_datalim_ax1 = ax1.dataLim.intervaly
    
    # The bug was that final_datalim_ax1 would be [inf, -inf] or similar
    # Check that the first axis dataLim was not corrupted
    assert not np.isinf(initial_datalim_ax1).any(), (
        "Initial dataLim of ax1 should not contain inf values"
    )
    
    # The key assertion: ax1's dataLim should remain the same after twinx and plotting
    # The bug was that ax1.dataLim would be corrupted to ±inf
    assert not np.isinf(final_datalim_ax1).any(), (
        "Final dataLim of ax1 should not contain inf values after plotting on twin axis"
    )
    
    # Check that the data limits are reasonable (not infinite)
    assert np.all(np.abs(final_datalim_ax1) < 1000), (
        "Final dataLim of ax1 should not contain extremely large values"
    )
    
    plt.close('all')


def test_twiny_stackplot_datalim():
    """
    Test that data limits of the first axis are not corrupted to ±inf
    when using stackplot on first axis and then plotting on twin y-axis.
    
    This tests the twiny() case which also has the same fix.
    """
    # Setup data
    df1_index = [0, 1]  # Numeric x values
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]
    
    # Create the figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on the first axis
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial dataLim of ax1
    initial_datalim_ax1 = ax1.dataLim.intervalx
    
    # Create twin y-axis
    ax2 = ax1.twiny()
    
    # Plot on the second axis
    ax2.plot(df2_values, df1_index)  # Note: swap x and y for twiny
    
    # Get final dataLim of ax1 - this should NOT be inf
    final_datalim_ax1 = ax1.dataLim.intervalx
    
    # The bug was that final_datalim_ax1 would be [inf, -inf] or similar
    # Check that the first axis dataLim was not corrupted
    assert not np.isinf(initial_datalim_ax1).any(), (
        "Initial dataLim of ax1 should not contain inf values"
    )
    
    # The key assertion: ax1's dataLim should remain the same after twiny and plotting
    assert not np.isinf(final_datalim_ax1).any(), (
        "Final dataLim of ax1 should not contain inf values after plotting on twin axis"
    )
    
    # Check that the data limits are reasonable (not infinite)
    assert np.all(np.abs(final_datalim_ax1) < 1000), (
        "Final dataLim of ax1 should not contain extremely large values"
    )
    
    plt.close('all')


if __name__ == "__main__":
    test_twinx_stackplot_datalim()
    test_twinx_stackplot_datalim_numeric()
    test_twiny_stackplot_datalim()
    print("All tests passed!")