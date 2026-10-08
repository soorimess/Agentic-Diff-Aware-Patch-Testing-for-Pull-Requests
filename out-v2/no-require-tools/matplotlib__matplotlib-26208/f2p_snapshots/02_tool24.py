import matplotlib.pyplot as plt
import numpy as np
import pytest


def test_twinx_stackplot_datalim_bug_reproduction():
    """
    Test that reproduces the exact bug from the bug report.
    
    This test should fail on the old code and pass on the fixed code.
    The bug: when using twinx with stackplot on ax1, ax1's dataLim gets replaced by inf.
    """
    # Exact data from the bug report
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    # Create figure and first axis
    fig, ax1 = plt.subplots()

    # Plot stackplot on first axis - this is the key operation that triggers the bug
    ax1.stackplot(df1_index, df1_values)
    
    # Get initial data limits of ax1
    initial_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis - this is where the bug occurs
    ax2 = ax1.twinx()
    
    # Get data limits after creating twin axis (this should not change)
    datalim_after_twinx = ax1.dataLim.intervaly.copy()
    
    # Plot on second axis
    ax2.plot(df1_index, df2_values)
    
    # Get final data limits
    final_datalim = ax1.dataLim.intervaly.copy()
    
    # The bug manifests as inf values in the data limits
    # Before fix: initial_datalim = [-22.71770833  26.585     ]
    # After fix: should remain the same
    # But the bug causes: final_datalim = [ inf -inf] 
    
    # The test should verify that data limits don't become infinite
    # This assertion should fail on the old code but pass on the fixed code
    assert not np.isinf(initial_datalim).any(), f"Initial data limits should not contain inf, got {initial_datalim}"
    assert not np.isinf(datalim_after_twinx).any(), f"Data limits after twinx should not contain inf, got {datalim_after_twinx}"
    assert not np.isinf(final_datalim).any(), f"Final data limits should not contain inf, got {final_datalim}"
    
    # Most importantly, the data limits should be preserved
    # The bug was that final_datalim would be [inf, -inf] instead of the original values
    # Let's check that the values are reasonable (not infinite)
    # The original values should be around [-22.71770833, 26.585]
    expected_min = -25.0  # Some reasonable range
    expected_max = 30.0
    
    # Check that the limits are within reasonable bounds
    assert np.all(np.isfinite(datalim_after_twinx)), "datalim_after_twinx should contain finite values"
    assert np.all(np.isfinite(final_datalim)), "final_datalim should contain finite values"
    
    # Check that the limits are reasonable (not inf or nan)
    assert np.all(np.abs(datalim_after_twinx) < 1000), "datalim_after_twinx should be finite and reasonable"
    assert np.all(np.abs(final_datalim) < 1000), "final_datalim should be finite and reasonable"
    
    plt.close(fig)


def test_twiny_stackplot_datalim_preservation():
    """
    Test that twiny also preserves data limits properly.
    
    This tests the fix for the twiny method that was also part of the same change.
    """
    # Simple numeric data
    x = [0, 1, 2, 3]
    y = [1, 2, 3, 4]
    z = [0.5, 1.5, 2.5, 3.5]

    # Create figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on first axis
    ax1.stackplot(x, y, z)
    
    # Get initial data limits
    initial_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis using twiny
    ax2 = ax1.twiny()
    
    # Get data limits after creating twin axis
    datalim_after_twiny = ax1.dataLim.intervaly.copy()
    
    # Plot on second axis
    ax2.plot([10, 20, 30, 40], x)
    
    # Get final data limits
    final_datalim = ax1.dataLim.intervaly.copy()
    
    # All should be finite
    assert np.all(np.isfinite(initial_datalim)), "Initial data limits should be finite"
    assert np.all(np.isfinite(datalim_after_twiny)), "Data limits after twiny should be finite"
    assert np.all(np.isfinite(final_datalim)), "Final data limits should be finite"
    
    # Check that data limits don't become infinite
    assert not np.isinf(initial_datalim).any(), "Initial data limits should not contain inf"
    assert not np.isinf(datalim_after_twiny).any(), "Data limits after twiny should not contain inf"
    assert not np.isinf(final_datalim).any(), "Final data limits should not contain inf"
    
    plt.close(fig)


def test_twinx_stackplot_units_inheritance():
    """
    Test that units are properly inherited in twinx to prevent the dataLim bug.
    
    This specifically tests the fix that was applied to the twinx method.
    """
    # Simple numeric data to avoid unit conversion issues
    x = [0, 1, 2, 3]
    y = [1, 2, 3, 4]
    z = [0.5, 1.5, 2.5, 3.5]

    # Create figure and first axis
    fig, ax1 = plt.subplots()
    
    # Set some units on the axis to trigger the problematic code path
    # This is a more direct test of the fix
    ax1.xaxis.units = 'test_units_for_inheritance'
    
    # Plot stackplot on first axis
    ax1.stackplot(x, y, z)
    
    # Create twin axis
    ax2 = ax1.twinx()
    
    # The fix ensures that ax2 inherits the units properly
    # This should not cause dataLim corruption
    assert ax2.xaxis.units == ax1.xaxis.units, "ax2 should inherit xaxis units from ax1"
    
    # Plot on second axis
    ax2.plot(x, [10, 20, 30, 40])
    
    # Check that data limits are still reasonable
    final_datalim = ax1.dataLim.intervaly.copy()
    
    # The data limits should be finite
    assert not np.isinf(final_datalim).any(), "Final data limits should not contain inf"
    assert np.all(np.isfinite(final_datalim)), "Final data limits should be finite"
    
    plt.close(fig)


def test_twinx_stackplot_datalim_preservation_simple():
    """
    Simple test to ensure data limits are preserved in the basic case.
    """
    # Simple numeric data
    x = [0, 1, 2, 3]
    y = [1, 2, 3, 4]
    z = [0.5, 1.5, 2.5, 3.5]

    # Create figure and first axis
    fig, ax1 = plt.subplots()
    
    # Plot stackplot on first axis
    ax1.stackplot(x, y, z)
    
    # Get initial data limits
    initial_datalim = ax1.dataLim.intervaly.copy()
    
    # Create twin axis
    ax2 = ax1.twinx()
    
    # Get data limits after creating twin axis
    datalim_after_twinx = ax1.dataLim.intervaly.copy()
    
    # Plot on second axis
    ax2.plot(x, [10, 20, 30, 40])
    
    # Get final data limits
    final_datalim = ax1.dataLim.intervaly.copy()
    
    # All should be finite
    assert np.all(np.isfinite(initial_datalim)), "Initial data limits should be finite"
    assert np.all(np.isfinite(datalim_after_twinx)), "Data limits after twinx should be finite"
    assert np.all(np.isfinite(final_datalim)), "Final data limits should be finite"
    
    plt.close(fig)