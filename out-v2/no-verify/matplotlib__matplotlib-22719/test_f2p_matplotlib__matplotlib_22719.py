"""
Regression test for matplotlib issue #22719
Test that empty data with categorical units doesn't trigger deprecation warning.
"""
import warnings
import matplotlib.pyplot as plt
from matplotlib._api import MatplotlibDeprecationWarning


def test_empty_data_with_categorical_units_no_warning():
    """
    Test that plotting empty data with categorical units doesn't raise
    a deprecation warning about passing numbers through unit converters.
    
    This is a regression test for issue #22719 where empty arrays would
    incorrectly trigger a deprecation warning.
    """
    # Create figure and axis
    fig, ax = plt.subplots()
    
    # Set up categorical units
    ax.xaxis.update_units(["a", "b"])
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not raise a deprecation warning
        ax.plot([], [])
        
        # Check that no MatplotlibDeprecationWarning about unit conversion was raised
        unit_conversion_warnings = [
            warning for warning in w 
            if (issubclass(warning.category, MatplotlibDeprecationWarning) and
                "Support for passing numbers through unit converters is deprecated" in str(warning.message))
        ]
        
        assert len(unit_conversion_warnings) == 0, (
            f"Unexpected deprecation warning: {unit_conversion_warnings[0].message if unit_conversion_warnings else 'None'}"
        )
        
    plt.close(fig)