"""
Test for NumPy 1.24 deprecation warnings in matplotlib.colors
This test ensures that colormap evaluation doesn't generate deprecation warnings
when dealing with edge cases that produce out-of-bound integer values.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt
import warnings

def test_colormap_no_numpy_deprecation_warnings():
    """
    Test that colormap evaluation does not generate NumPy 1.24 deprecation warnings
    for out-of-bound integer conversions.
    
    This test specifically addresses the issue where certain inputs to colormaps
    would generate deprecation warnings about conversion of out-of-bound integers
    due to the placement of np.errstate context manager in the codebase.
    """
    # Capture warnings to ensure no deprecation warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Test case from the bug report
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check specifically for the key numpy deprecation warning 
        deprecation_warnings = []
        for warn in w:
            warning_text = str(warn.message).lower()
            if 'conversion of out-of-bound' in warning_text:
                deprecation_warnings.append(warn)
            
        # If there are any deprecation warnings about out-of-bound conversions,
        # the fix hasn't been applied properly
        assert len(deprecation_warnings) == 0, (
            f"Found NumPy deprecation warnings about out-of-bound conversions: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )