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
    
    # Test that using base raises FutureWarning
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', base=6).mean()
    
    # The result should still work but with a warning
    assert isinstance(result, xr.DataArray)


def test_resample_loffset_deprecation_warning():
    """Test that using loffset parameter raises deprecation warning."""
    # Create a simple datetime index
    index = pd.date_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[index], dims=['time'])
    
    # Test that using loffset raises FutureWarning
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', loffset='12H').mean()
    
    # The result should still work but with a warning
    assert isinstance(result, xr.DataArray)


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
    with pytest.raises(ValueError, match="`loffset` must be"):
        da.resample(time='2D', loffset=123).mean()


def test_resample_cftime_with_base():
    """Test that base parameter works with cftime indexes."""
    # Create a cftime index
    cftime_index = xr.cftime_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[cftime_index], dims=['time'])
    
    # Test that using base raises FutureWarning for cftime
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', base=6).mean()
    
    # The result should still work but with a warning
    assert isinstance(result, xr.DataArray)


def test_resample_cftime_with_loffset():
    """Test that loffset parameter works with cftime indexes."""
    # Create a cftime index
    cftime_index = xr.cftime_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[cftime_index], dims=['time'])
    
    # Test that using loffset raises FutureWarning for cftime
    with pytest.warns(FutureWarning):
        result = da.resample(time='2D', loffset='12H').mean()
    
    # The result should still work but with a warning
    assert isinstance(result, xr.DataArray)


def test_resample_cftime_loffset_validation():
    """Test that loffset validation works with cftime indexes."""
    # Create a cftime index
    cftime_index = xr.cftime_range('2000-01-01', periods=10, freq='D')
    da = xr.DataArray(np.arange(10.0), coords=[cftime_index], dims=['time'])
    
    # Test that invalid loffset raises ValueError even for cftime
    with pytest.raises(ValueError, match="`loffset` must be"):
        da.resample(time='2D', loffset=123).mean()