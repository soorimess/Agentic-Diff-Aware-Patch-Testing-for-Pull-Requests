import numpy as np
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over DataArrayRolling gives same result as .mean() when center=True"""
    
    # Create test data - using exact example from bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Get the result from the .mean() method (expected behavior)
    result_mean = my_data.rolling(x=3, center=True).mean()
    
    # Get result from manual iteration 
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iterated = [window.mean().values.item() for label, window in my_data_rolling]
    
    # Check that both results have the same length
    assert len(result_iterated) == len(result_mean.values)
    
    # Check the non-NaN values match - they should be positioned identically
    # Extract non-NaN values
    expected_non_nan = [2., 3., 4., 5., 6., 7., 8.]
    actual_non_nan = [val for val in result_iterated if not np.isnan(val)]
    
    # Verify the non-NaN values from iteration match what .mean() produces
    for i, (exp, act) in enumerate(zip(expected_non_nan, actual_non_nan)):
        assert np.isclose(exp, act), f"Non-NaN value {i}: expected {exp} but got {act}"
        
    # Check the positions where we should get NaN (end points)
    # With center=True, NaN should only be at the beginning and end
    mean_result_array = result_mean.values
    nan_positions_expected = [i for i, val in enumerate(mean_result_array) if np.isnan(val)]
    nan_positions_actual = [i for i, val in enumerate(result_iterated) if np.isnan(val)]
    
    assert nan_positions_expected == nan_positions_actual, f"NaN positions don't match. Expected: {nan_positions_expected}, Got: {nan_positions_actual}"


def test_rolling_center_iteration_edge_cases():
    """Test rolling center iteration with different window sizes and data"""
    
    # Test with even window size
    data = xr.DataArray(np.arange(1, 9), dims="x")
    result_mean = data.rolling(x=4, center=True).mean()
    rolling_obj = data.rolling(x=4, center=True)
    result_iterated = [window.mean().values.item() for label, window in rolling_obj]
    
    # Should produce valid means for central windows, NaN elsewhere
    # Compare that both give same pattern of nans
    mean_result_array = result_mean.values
    nan_positions_expected = [i for i, val in enumerate(mean_result_array) if np.isnan(val)]
    nan_positions_actual = [i for i, val in enumerate(result_iterated) if np.isnan(val)]
    
    assert nan_positions_expected == nan_positions_actual
    
    # Test with small data and window - single center value 
    data2 = xr.DataArray([1, 2, 3], dims="x")
    result_mean2 = data2.rolling(x=3, center=True).mean()
    rolling_obj2 = data2.rolling(x=3, center=True)
    result_iterated2 = [window.mean().values.item() for label, window in rolling_obj2]
    
    mean_result_array2 = result_mean2.values
    nan_positions_expected2 = [i for i, val in enumerate(mean_result_array2) if np.isnan(val)]
    nan_positions_actual2 = [i for i, val in enumerate(result_iterated2) if np.isnan(val)]
    
    assert nan_positions_expected2 == nan_positions_actual2