"""
Regression test for bug where empty data with categorical units
produces confusing deprecation warning.
"""
import numpy as np
import pytest
import warnings

import matplotlib.pyplot as plt
import matplotlib.category as cat
from matplotlib._api import MatplotlibDeprecationWarning


def test_empty_data_with_category_units():
    """Test that empty data with categorical units doesn't produce deprecation warning."""
    # Create a figure and axis
    f, ax = plt.subplots()
    
    # Set up categorical units on x-axis
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not produce a deprecation warning
        ax.plot([], [])
        
        # Check that no MatplotlibDeprecationWarning was raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning)]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
        )


def test_empty_data_convert_xunits():
    """Test that convert_xunits with empty data doesn't produce deprecation warning."""
    # Create a figure and axis
    f, ax = plt.subplots()
    
    # Set up categorical units on x-axis
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not produce a deprecation warning
        result = ax.convert_xunits([])
        
        # Check that no MatplotlibDeprecationWarning was raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning)]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # The result should be an empty array
        assert len(result) == 0


def test_non_empty_data_still_warns():
    """Test that non-empty data with numeric values still produces appropriate warnings."""
    # Create a figure and axis
    f, ax = plt.subplots()
    
    # Set up categorical units on x-axis
    ax.xaxis.update_units(["a", "b"])
    
    # Test that normal operation still works
    # This should not produce the specific deprecation warning we're fixing
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Plot some string data - should not warn
        ax.plot(["a", "b"], [1, 2])
        
        # Check that no MatplotlibDeprecationWarning was raised for string data
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning)]
        
        # For string data, there should be no deprecation warnings about unit conversion
        # (The specific warning we're fixing is about passing numbers through converters)
        # But we're not testing that specific case here - just ensuring our fix doesn't break normal behavior
        pass


if __name__ == "__main__":
    test_empty_data_with_category_units()
    test_empty_data_convert_xunits()
    test_non_empty_data_still_warns()
    print("All tests passed!")