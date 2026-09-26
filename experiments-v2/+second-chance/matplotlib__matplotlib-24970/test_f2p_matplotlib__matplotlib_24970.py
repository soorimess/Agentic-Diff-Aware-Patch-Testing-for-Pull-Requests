"""
Test for NumPy 1.24 deprecation warnings in colormap handling.

This test ensures that calling a colormap with out-of-bounds values
does not produce NumPy deprecation warnings about conversion of
out-of-bound Python integers to integer arrays.
"""
import numpy as np
import warnings
from matplotlib import colormaps


def test_colormap_no_deprecation_warnings():
    """
    Test that colormap calls don't produce NumPy 1.24 deprecation warnings.
    
    This is a regression test for the issue where calling a colormap with
    out-of-bounds values would produce deprecation warnings about
    NumPy's conversion of out-of-bound Python integers to integer arrays.
    """
    # Create a standard colormap using the new API
    cmap = colormaps.get_cmap('viridis')
    
    # Test with the exact case from the bug report that was causing warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This is the exact case from the bug report that was triggering warnings
        result = cmap(np.empty((0,), dtype=np.uint8))
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        
        # There should be no deprecation warnings
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warning.message) for warning in deprecation_warnings]}"
        )


def test_colormap_with_out_of_bounds_values_no_warnings():
    """
    Test that colormap calls with out-of-bounds values don't produce warnings.
    """
    # Create a colormap using the new API
    cmap = colormaps.get_cmap('viridis')
    
    # Test with values that would trigger out-of-bounds assignment paths
    # These should not produce deprecation warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Test with values that would be clipped to out-of-bounds
        test_values = np.array([256, 257, 258], dtype=np.float64)
        result = cmap(test_values)
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        
        # There should be no deprecation warnings
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warning.message) for warning in deprecation_warnings]}"
        )