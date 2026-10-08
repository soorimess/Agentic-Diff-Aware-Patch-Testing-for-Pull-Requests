"""
Regression test for matplotlib issue with confusing deprecation warning
when empty data is passed to axis with category units.

This test ensures that empty data does not trigger the deprecation warning
about passing numbers through unit converters.
"""

import matplotlib.pyplot as plt
import warnings
import numpy as np
import pytest
from matplotlib._api.deprecation import MatplotlibDeprecationWarning


def test_empty_data_with_category_units_no_deprecation_warning():
    """
    Test that plotting empty data with category units does not produce
    a confusing deprecation warning.
    
    This is a regression test for the bug where empty data would trigger
    a deprecation warning about passing numbers through unit converters,
    even though there are no numbers to convert.
    """
    # Create figure and axis
    f, ax = plt.subplots()
    
    # Set up category units
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not produce a deprecation warning
        ax.plot([], [])
        
        # Check that no deprecation warning was raised about unit conversion
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message).lower() and
                               "unit" in str(warning.message).lower()]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings about units: {[str(w.message) for w in deprecation_warnings]}"
        )


def test_empty_data_with_category_units_no_conversion_error():
    """
    Test that plotting empty data with category units does not raise
    a ConversionError.
    """
    # Create figure and axis
    f, ax = plt.subplots()
    
    # Set up category units
    ax.xaxis.update_units(["a", "b"])
    
    # This should not raise an exception
    try:
        ax.plot([], [])
        # If we get here without exception, that's good
    except Exception as e:
        # If we get a conversion error, that's the bug
        if "ConversionError" in str(type(e)):
            # If this is the specific bug we're fixing, we should not get this error
            raise AssertionError(f"Unexpected conversion error: {e}")


def test_empty_data_convert_xunits_no_deprecation_warning():
    """
    Test that calling convert_xunits with empty data does not produce
    a deprecation warning.
    """
    # Create figure and axis
    f, ax = plt.subplots()
    
    # Set up category units
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not produce a deprecation warning
        result = ax.convert_xunits([])
        
        # Check that no deprecation warning was raised about unit conversion
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message).lower() and
                               "unit" in str(warning.message).lower()]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings about units: {[str(w.message) for w in deprecation_warnings]}"
        )


if __name__ == "__main__":
    test_empty_data_with_category_units_no_deprecation_warning()
    test_empty_data_with_category_units_no_conversion_error()
    test_empty_data_convert_xunits_no_deprecation_warning()
    print("All tests passed!")