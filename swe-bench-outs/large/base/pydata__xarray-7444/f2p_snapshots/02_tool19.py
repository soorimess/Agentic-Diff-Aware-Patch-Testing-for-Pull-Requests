"""
Regression tests for pull request that deprecates base and loffset parameters in resample.

This tests the behavior changes introduced in the pull request:
- base parameter is deprecated and converted to offset
- loffset parameter is deprecated and issues warnings
- base and offset cannot be used together
- New TimeResampleGrouper class handles both regular and CFTime cases
"""

import numpy as np
import pandas as pd
import pytest
import warnings

import xarray as xr
from xarray import DataArray


def test_resample_base_parameter_deprecation_warning():
    """Test that using base parameter raises deprecation warning."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Should emit a warning when base is used (old behavior)
    with pytest.warns(FutureWarning, match=".*base.*deprecated.*"):
        result = da.resample(time="2D", base=3)
        # Just test that it runs without error
        result.mean()


def test_resample_loffset_parameter_deprecation_warning():
    """Test that using loffset parameter raises deprecation warning."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Should emit a warning when loffset is used (old behavior)
    with pytest.warns(FutureWarning, match=".*loffset.*deprecated.*"):
        result = da.resample(time="2D", loffset="1D")
        # Just test that it runs without error
        result.mean()


def test_resample_base_and_offset_error():
    """Test that using both base and offset raises ValueError with new message."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # After the change, should raise ValueError with consistent message
    # The new error message is "base and offset cannot be present at the same time"
    with pytest.raises(ValueError, match="base and offset cannot be present at the same time"):
        da.resample(time="2D", base=3, offset="1D")


def test_resample_base_conversion_to_offset():
    """Test that base parameter is properly converted to offset."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Test that base parameter works and gets converted to offset
    # This should not raise an error and should produce valid results
    result = da.resample(time="2D", base=6)
    # Just test that it runs without error
    result.mean()


def test_resample_origin_and_offset_work():
    """Test that origin and offset parameters work correctly."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Test that origin and offset work without warnings
    result = da.resample(time="2D", origin="start_day", offset="6H")
    # Just test that it runs without error
    result.mean()


def test_resample_base_deprecation_warning_message():
    """Test that the deprecation warning for base has the correct message."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Should emit a specific warning message about base deprecation
    with pytest.warns(FutureWarning) as warning_list:
        da.resample(time="2D", base=3)
        # Check that warning message contains expected text
        warning_messages = [str(warning.message) for warning in warning_list]
        assert any("base" in msg.lower() and "deprecated" in msg.lower() for msg in warning_messages)


def test_resample_loffset_deprecation_warning_message():
    """Test that the deprecation warning for loffset has the correct message."""
    # Create test data with datetime index
    times = pd.date_range("2000-01-01", periods=10, freq="D")
    da = DataArray(np.arange(10), dims=["time"], coords={"time": times})
    
    # Should emit a specific warning message about loffset deprecation
    with pytest.warns(FutureWarning) as warning_list:
        da.resample(time="2D", loffset="1D")
        # Check that warning message contains expected text
        warning_messages = [str(warning.message) for warning in warning_list]
        assert any("loffset" in msg.lower() and "deprecated" in msg.lower() for msg in warning_messages)