"""
Regression test for matplotlib issue #22719:
Confusing deprecation warning when empty data passed to axis with category units
"""
import matplotlib.pyplot as plt
import numpy as np
import warnings
from matplotlib._api import MatplotlibDeprecationWarning


def test_empty_data_with_category_units_no_deprecation_warning():
    """
    Test that empty data with category units doesn't produce deprecation warnings.
    
    The bug: When calling ax.plot([], []) with category units, it incorrectly 
    issued a deprecation warning about passing numbers through unit converters.
    
    The fix: Added check for values.size to prevent issuing warning for empty data.
    """
    # This should not produce a deprecation warning
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ax.plot([], [])
        
        # Check that no deprecation warning was raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message)]
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning with empty data: {[str(w.message) for w in deprecation_warnings]}"
        )


def test_empty_data_convert_units_no_deprecation_warning():
    """
    Test that convert_units with empty data doesn't produce deprecation warnings.
    
    This tests the same issue but for direct convert_units calls.
    """
    # This should not produce a deprecation warning
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ax.convert_xunits([])
        
        # Check that no deprecation warning was raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message)]
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning with convert_xunits and empty data: {[str(w.message) for w in deprecation_warnings]}"
        )


def test_empty_data_with_numeric_units_no_warning():
    """
    Test that empty data with numeric units works correctly (no units).
    """
    f, ax = plt.subplots()
    # Don't set category units, let it be numeric
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ax.plot([], [])
        
        # Should not have deprecation warnings for normal numeric data
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message)]
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning with numeric data: {[str(w.message) for w in deprecation_warnings]}"
        )


def test_non_empty_string_data_with_category_units():
    """
    Test that non-empty string data with category units works correctly.
    """
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    
    # This should work normally with string data
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ax.plot(["a", "b"], [1, 2])
        
        # Check that no deprecation warning was raised for valid string data
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, MatplotlibDeprecationWarning) and 
                               "deprecated" in str(warning.message)]
        assert len(deprecation_warnings) == 0, (
            f"Unexpected deprecation warning with string data: {[str(w.message) for w in deprecation_warnings]}"
        )