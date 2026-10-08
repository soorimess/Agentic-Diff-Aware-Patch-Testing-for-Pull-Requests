"""
Test for regression of deprecation warning with empty data and category units.

This test ensures that when plotting empty data with categorical units,
no deprecation warning is issued.
"""

import matplotlib.pyplot as plt
import warnings
from matplotlib._api.deprecation import MatplotlibDeprecationWarning


def test_empty_data_with_category_units_no_warning():
    """Test that empty data with categorical units doesn't produce deprecation warning."""
    # Create figure and axis
    f, ax = plt.subplots()
    
    # Set up categorical units - this is the key part from the bug report
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should NOT produce a deprecation warning (the bug)
        ax.plot([], [])
        
        # Check that no deprecation warning was issued
        deprecation_warnings = [warning for warning in w 
                               if warning.category is MatplotlibDeprecationWarning and 
                               'deprecated' in str(warning.message).lower()]
        
        # This should pass after the fix is applied
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning for empty data: {deprecation_warnings[0].message if deprecation_warnings else 'None'}"
        )


def test_empty_data_convert_xunits_no_warning():
    """Test that convert_xunits with empty data doesn't produce deprecation warning."""
    # Create figure and axis
    f, ax = plt.subplots()
    
    # Set up categorical units
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should NOT produce a deprecation warning
        result = ax.convert_xunits([])
        
        # Check that no deprecation warning was issued
        deprecation_warnings = [warning for warning in w 
                               if warning.category is MatplotlibDeprecationWarning and 
                               'deprecated' in str(warning.message).lower()]
        
        # This should pass after the fix is applied
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning for empty data in convert_xunits: {deprecation_warnings[0].message if deprecation_warnings else 'None'}"
        )