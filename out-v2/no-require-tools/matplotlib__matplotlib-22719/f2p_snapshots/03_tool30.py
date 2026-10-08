"""
Regression test for bug where empty data with categorical units
produces confusing deprecation warning.
"""
import warnings

import matplotlib.pyplot as plt
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