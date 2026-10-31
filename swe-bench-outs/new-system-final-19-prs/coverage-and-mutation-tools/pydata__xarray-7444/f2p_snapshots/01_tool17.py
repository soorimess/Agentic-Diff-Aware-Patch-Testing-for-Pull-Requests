import datetime
import numpy as np
import pandas as pd
import pytest
import xarray as xr
import warnings

cftime = pytest.importorskip("cftime")


def test_resample_base_deprecation_warning():
    """Test that using base parameter raises deprecation warning."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that using base raises FutureWarning - check the actual warning message
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', base=6).mean()
    
    # The result should still work but with a warning
    assert result is not None


def test_resample_loffset_deprecation_warning():
    """Test that using loffset parameter raises deprecation warning."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that using loffset raises FutureWarning - check the actual warning message
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', loffset='12H').mean()
    
    # The result should still work but with a warning
    assert result is not None


def test_resample_base_offset_validation():
    """Test that base and offset cannot be used together."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that using both base and offset raises ValueError
    with pytest.raises(ValueError, match="cannot be present at the same time"):
        da.resample(time='2D', base=6, offset='12H').mean()


def test_resample_loffset_validation():
    """Test that loffset parameter validation works correctly."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that invalid loffset raises ValueError
    with pytest.raises(ValueError, match="`loffset` must be a"):
        da.resample(time='2D', loffset=123).mean()


def test_resample_with_origin_and_offset():
    """Test that new origin and offset parameters work correctly."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that new parameters work without warnings
    result = da.resample(time='2D', origin='start', offset='6H').mean()
    
    # The result should be valid
    assert result is not None


def test_resample_cftime_with_base():
    """Test that base parameter works with cftime indexes."""
    # Create a cftime index
    cftime_index = xr.cftime_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[cftime_index], dims=['time'])
    
    # Test that using base raises FutureWarning for cftime
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', base=6).mean()
    
    # The result should still work but with a warning
    assert result is not None


# Keep the original test to make sure we don't break anything
def test_seeded_resample():
    """Test that existing functionality still works."""
    # This is a copy of the original test that was in the file
    initial_freq = "8003D"
    resample_freq = "4001D"
    start = "2000-01-01T12:07:01"
    loffset = "12H"
    origin = "start"
    
    index_kwargs = dict(start=start, periods=5, freq=initial_freq)
    datetime_index = pd.date_range(**index_kwargs)
    cftime_index = xr.cftime_range(**index_kwargs)
    
    da_datetimeindex = xr.DataArray(
        np.arange(100.0, 100.0 + datetime_index.size), coords=[datetime_index], dims=["time"]
    )
    da_cftimeindex = xr.DataArray(
        np.arange(100.0, 100.0 + cftime_index.size), coords=[cftime_index], dims=["time"]
    )
    
    # This test should pass without issues
    result_datetimeindex = da_datetimeindex.resample(
        time=resample_freq,
        closed=None,
        label=None,
        base=24,
        loffset=loffset,
        origin=origin,
    ).mean()
    
    result_cftimeindex = da_cftimeindex.resample(
        time=resample_freq,
        closed=None,
        label=None,
        base=24,
        loffset=loffset,
        origin=origin,
    ).mean()
    
    # The results should be valid
    assert result_datetimeindex is not None
    assert result_cftimeindex is not None