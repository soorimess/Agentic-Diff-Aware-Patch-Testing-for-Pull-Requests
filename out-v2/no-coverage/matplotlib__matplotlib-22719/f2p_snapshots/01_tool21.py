"""
Regression test for matplotlib issue #22719.

This test ensures that when empty data is passed to an axis with category units,
no confusing deprecation warning is issued.
"""

import matplotlib.pyplot as plt
import warnings
import numpy as np
from matplotlib._api import MatplotlibDeprecationWarning


def test_empty_data_with_category_units_no_warning():
    """
    Test that plotting empty data with category units doesn't issue
    deprecation warnings.
    
    This is a regression test for issue #22719 where a confusing
    deprecation warning was issued when plotting empty data on axes
    with category units.
    """
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Set up the problematic scenario from the bug report
        f, ax = plt.subplots()
        ax.xaxis.update_units(["a", "b"])
        ax.plot([], [])
        
        # Check that no deprecation warnings about unit conversion were issued
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) 
                               and 'deprecated' in str(warning.message).lower()
                               and 'unit' in str(warning.message).lower()]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings about unit conversion: "
            f"{[str(w.message) for w in deprecation_warnings]}"
        )


def test_empty_data_convert_xunits_no_warning():
    """
    Test that calling convert_xunits with empty data doesn't issue
    deprecation warnings.
    """
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Set up the problematic scenario from the bug report
        f, ax = plt.subplots()
        ax.xaxis.update_units(["a", "b"])
        
        # This should not issue deprecation warnings either
        ax.convert_xunits([])
        
        # Check that no deprecation warnings about unit conversion were issued
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) 
                               and 'deprecated' in str(warning.message).lower()
                               and 'unit' in str(warning.message).lower()]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings about unit conversion: "
            f"{[str(w.message) for w in deprecation_warnings]}"
        )


def test_empty_data_direct_convert_no_warning():
    """
    Test that directly calling the convert function with empty data
    doesn't issue deprecation warnings.
    """
    from matplotlib.category import StrCategoryConverter, UnitData
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Set up unit data
        unit_data = UnitData(["a", "b"])
        
        # This should not issue deprecation warnings for empty data
        result = StrCategoryConverter.convert([], unit_data, None)
        
        # Check that no deprecation warnings about unit conversion were issued
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) 
                               and 'deprecated' in str(warning.message).lower()
                               and 'unit' in str(warning.message).lower()]
        
        # There should be no deprecation warnings about unit conversion
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warnings about unit conversion: "
            f"{[str(w.message) for w in deprecation_warnings]}"
        )


if __name__ == "__main__":
    test_empty_data_with_category_units_no_warning()
    test_empty_data_convert_xunits_no_warning()
    test_empty_data_direct_convert_no_warning()
    print("All tests passed!")