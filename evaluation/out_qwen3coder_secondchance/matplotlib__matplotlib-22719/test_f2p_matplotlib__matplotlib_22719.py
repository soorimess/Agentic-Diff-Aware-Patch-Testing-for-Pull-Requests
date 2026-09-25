"""
Regression test for matplotlib issue #22719

This test specifically verifies that the fix for confusing deprecation 
warning when empty data is passed to axis with category units works correctly.

The bug was that when empty data is passed to axes with category units,
deprecation warnings were incorrectly issued even for empty data.
"""

import matplotlib.pyplot as plt
import warnings


def test_empty_data_no_deprecation_warning():
    """
    Test that empty data does NOT trigger deprecation warning for numeric
    pass-through through category converters.
    
    This is the main bug fix: empty arrays should not produce warnings.
    
    Behavior being tested:
    - BEFORE fix: Empty arrays [] would incorrectly trigger deprecation warning
    - AFTER fix: Empty arrays [] should not trigger deprecation warning
    """
    # Setup axis with category units
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b", "c"])
    
    # Capture all warnings to verify no unwanted deprecation warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Plot with empty data - this should not warn (this was the bug)
        ax.plot([], [])
        
        # Filter for the specific warning we're testing
        numeric_warnings = [
            warning for warning in w
            if 'numbers through unit converters' in str(warning.message) and
               'deprecated' in str(warning.message).lower()
        ]
        
        # The fix prevents this warning for empty data
        assert len(numeric_warnings) == 0, (
            "Empty data should not trigger numeric pass-through deprecation warning. "
            f"Got warnings: {[str(w.message) for w in numeric_warnings]}"
        )


if __name__ == "__main__":
    test_empty_data_no_deprecation_warning()
    print("Test passed - empty data correctly doesn't warn about numeric pass-through")