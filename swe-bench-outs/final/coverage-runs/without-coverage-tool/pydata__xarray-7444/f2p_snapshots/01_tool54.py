"""Test for the deprecation of base and loffset parameters in resample.

This test ensures that the new TimeResampleGrouper class exists and works properly,
and that the deprecation warnings are raised when using deprecated parameters.
"""

import warnings

import numpy as np
import pandas as pd
import pytest

import xarray as xr
from xarray import DataArray


def test_time_resample_grouper_exists():
    """Test that TimeResampleGrouper class exists and can be imported."""
    # This should work after the change is applied
    from xarray.core.groupby import TimeResampleGrouper
    assert TimeResampleGrouper is not None


def test_resample_base_deprecation_warning():
    """Test that using base parameter raises deprecation warning."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # This should raise a FutureWarning about base being deprecated
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="24H", base=6).mean()
        
        # Check that a warning was raised about base deprecation
        warning_messages = [str(warning.message) for warning in w]
        base_deprecation_warnings = [
            msg for msg in warning_messages 
            if "base" in msg and "deprecated" in msg.lower()
        ]
        assert len(base_deprecation_warnings) >= 1


def test_resample_loffset_deprecation_warning():
    """Test that using loffset parameter raises deprecation warning."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # This should raise a FutureWarning about loffset being deprecated
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="24H", loffset="-12H").mean()
        
        # Check that a warning was raised about loffset deprecation
        warning_messages = [str(warning.message) for warning in w]
        loffset_deprecation_warnings = [
            msg for msg in warning_messages 
            if "loffset" in msg and "deprecated" in msg.lower()
        ]
        assert len(loffset_deprecation_warnings) >= 1


def test_resample_base_offset_validation():
    """Test that using both base and offset raises ValueError."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # This should raise a ValueError when both base and offset are provided
    with pytest.raises(ValueError, match="base and offset cannot be present at the same time"):
        array.resample(time="24H", base=6, offset="6H").mean()


def test_resample_basic_functionality():
    """Test that basic resample functionality still works."""
    times = pd.date_range("2000-01-01", freq="6H", periods=10)
    array = DataArray(np.arange(10), [("time", times)])
    
    # Basic resample should work without warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = array.resample(time="24H").mean()
        
        # Should not raise deprecation warnings for normal usage
        warning_messages = [str(warning.message) for warning in w]
        deprecation_warnings = [
            msg for msg in warning_messages 
            if "deprecated" in msg.lower()
        ]
        assert len(deprecation_warnings) == 0
        assert result is not None