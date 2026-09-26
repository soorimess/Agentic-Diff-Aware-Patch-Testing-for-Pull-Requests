"""
Test for NumPy 1.24 deprecation warnings in colormap handling.

This test verifies that calling a colormap with uint8 arrays
does not produce NumPy deprecation warnings about out-of-bound
Python integers to integer arrays conversion.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_uint8_no_deprecation_warnings():
    """
    Test that uint8 arrays don't produce NumPy deprecation warnings.
    
    This addresses the bug where NumPy 1.24+ issues deprecation warnings
    when converting out-of-bound Python integers to integer arrays.
    """
    # Test the exact reproduction case from the bug report
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not produce any deprecation warnings
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check that no NumPy deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if (issubclass(warning.category, np.VisibleDeprecationWarning) 
                                   or "out-of-bound" in str(warning.message))]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} NumPy deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we get a proper result
        assert result.shape == (0, 4)


def test_colormap_uint8_with_values_no_deprecation_warnings():
    """
    Test that uint8 arrays with actual values don't produce warnings.
    """
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Test with actual uint8 values
        test_data = np.array([0, 128, 255], dtype=np.uint8)
        result = plt.get_cmap()(test_data)
        
        # Check that no NumPy deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if (issubclass(warning.category, np.VisibleDeprecationWarning) 
                                   or "out-of-bound" in str(warning.message))]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} NumPy deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we get a proper result
        assert result.shape == (3, 4)


def test_colormap_float_with_out_of_bounds_no_deprecation_warnings():
    """
    Test that float arrays with out-of-bounds values don't produce warnings.
    """
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Test with float values that will be out of bounds
        test_data = np.array([-1.0, 2.0, 1.5], dtype=np.float64)
        result = plt.get_cmap()(test_data)
        
        # Check that no NumPy deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if (issubclass(warning.category, np.VisibleDeprecationWarning) 
                                   or "out-of-bound" in str(warning.message))]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} NumPy deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we get a proper result
        assert result.shape == (3, 4)