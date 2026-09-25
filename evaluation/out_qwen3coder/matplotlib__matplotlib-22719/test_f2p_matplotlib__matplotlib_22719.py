"""
Regression test for matplotlib bug:
Confusing deprecation warning when empty data passed to axis with category units
"""
import matplotlib.pyplot as plt
import warnings


def test_no_deprecation_warning_for_empty_data_with_category_units():
    """
    Test that plotting empty data with category units doesn't produce
    a confusing deprecation warning about passing numbers through unit converters.
    
    This is a regression test for the bug where ax.plot([], []) would issue
    a deprecation warning even though no numbers are being passed through.
    """
    # Set up exactly as described in the bug report
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings and make sure we detect the specific case 
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This exact call was triggering the bug
        ax.plot([], [])
        
        # Filter for the _exact_ warning mentioned in the bug report
        deprecation_warnings = [
            warning for warning in w 
            if ('deprecated' in str(warning.message).lower() and
                'numbers through unit converters' in str(warning.message))
        ]
        
        # This should not produce any such warnings 
        assert len(deprecation_warnings) == 0, (
            "Bug still present: deprecation warning incorrectly issued for empty data with category units. "
            f"Got {len(deprecation_warnings)} warnings: {[str(w.message) for w in deprecation_warnings]}"
        )


if __name__ == "__main__":
    test_no_deprecation_warning_for_empty_data_with_category_units()
    print("Test passes - bug is fixed or test is correctly written")