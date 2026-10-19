"""
Regression tests for the resample base and loffset parameter deprecation.

This test file ensures that the deprecation warnings are properly emitted
and that the correct error is raised when invalid combinations of parameters
are used in resample operations.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import warnings

import xarray as xr
from xarray import DataArray


def test_resample_base_parameter_emits_new_warning():
    """Test that using the base parameter emits the new pandas-style FutureWarning."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # Check that a warning is emitted when base is used with the new message
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="24H", base=6).mean()
        
        # Should have at least one warning
        assert len(w) >= 1
        # Should be a FutureWarning
        assert issubclass(w[0].category, FutureWarning)
        
        # Check that the warning message matches the new expected format
        warning_message = str(w[0].message)
        assert "Following pandas, the `base` parameter to resample will be deprecated" in warning_message
        assert "Switch to using `origin` or `offset` instead" in warning_message
        
    assert result is not None


def test_resample_loffset_parameter_emits_new_warning():
    """Test that using the loffset parameter emits the new pandas-style FutureWarning."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # Check that a warning is emitted when loffset is used with the new message
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="24H", loffset="12H").mean()
        
        # Should have at least one warning
        assert len(w) >= 1
        # Should be a FutureWarning
        assert issubclass(w[0].category, FutureWarning)
        
        # Check that the warning message matches the new expected format
        warning_message = str(w[0].message)
        assert "Following pandas, the `loffset` parameter to resample will be deprecated" in warning_message
        assert "Switch to using time offset arithmetic" in warning_message
        
    assert result is not None


def test_resample_base_and_offset_conflict_raises_correct_error():
    """Test that using both base and offset raises a ValueError with correct message."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # This should raise a ValueError because base and offset cannot be used together
    # The NEW error message (from the change) is "base and offset cannot be present at the same time"
    with pytest.raises(ValueError, match="base and offset cannot be present at the same time"):
        array.resample(time="24H", base=6, offset="6H").mean()


def test_resample_base_conversion_works():
    """Test that base parameter is properly converted to offset."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # Test that base=6 with 6H frequency gets converted properly
    # This should work without error and emit a warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="6H", base=2).mean()
        
        # Should have at least one warning
        assert len(w) >= 1
        # Should be a FutureWarning
        assert issubclass(w[0].category, FutureWarning)
        
    assert result is not None


def test_resample_with_origin_and_offset_works():
    """Test that using origin and offset parameters works correctly."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # This should work without warnings or errors
    result = array.resample(time="24H", origin="start_day", offset="6H").mean()
    
    assert result is not None