import datetime
import numpy as np
import pandas as pd
import pytest
import xarray as xr

cftime = pytest.importorskip("cftime")


def test_resample_base_deprecation_warning():
    """Test that using base parameter raises deprecation warning."""
    # Create a simple datetime index
    index = pd.date_range("2000-01-01", periods=10, freq="D")
    da = xr.DataArray(np.arange(10), coords=[index], dims=["time"])
    
    # This should emit a FutureWarning about base being deprecated
    with pytest.warns(FutureWarning, match="base.*deprecated"):
        result = da.resample(time="2D", base=6).mean()
    
    # The result should still work and have expected shape
    assert result is not None
    assert result.shape == (5,)


def test_resample_loffset_deprecation_warning():
    """Test that using loffset parameter raises deprecation warning."""
    # Create a simple datetime index
    index = pd.date_range("2000-01-01", periods=10, freq="D")
    da = xr.DataArray(np.arange(10), coords=[index], dims=["time"])
    
    # This should emit a FutureWarning about loffset being deprecated
    with pytest.warns(FutureWarning, match="loffset.*deprecated"):
        result = da.resample(time="2D", loffset="1D").mean()
    
    # The result should still work and have expected shape
    assert result is not None
    assert result.shape == (5,)


def test_resample_base_offset_conflict_error():
    """Test that using both base and offset raises ValueError."""
    # Create a simple datetime index
    index = pd.date_range("2000-01-01", periods=10, freq="D")
    da = xr.DataArray(np.arange(10), coords=[index], dims=["time"])
    
    # This should raise a ValueError
    with pytest.raises(ValueError, match=".*and.*cannot be present at the same time.*"):
        da.resample(time="2D", base=6, offset="1D").mean()


def test_resample_loffset_validation():
    """Test that loffset parameter validation works correctly."""
    # Create a simple datetime index
    index = pd.date_range("2000-01-01", periods=10, freq="D")
    da = xr.DataArray(np.arange(10), coords=[index], dims=["time"])
    
    # Test invalid loffset type
    with pytest.raises(ValueError, match="loffset.*must be"):
        da.resample(time="2D", loffset=123).mean()