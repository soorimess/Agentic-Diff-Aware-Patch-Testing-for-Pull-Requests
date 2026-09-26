"""
Test for matplotlib bug related to NumPy 1.24 deprecation warnings.

This test ensures that the colormap's __call__ method does not produce
NumPy deprecation warnings when dealing with out-of-bound integer assignments
to uint8 arrays.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_uint8_deprecation_warnings():
    """
    Test that colormap __call__ does not produce NumPy 1.24 deprecation warnings
    when assigning out-of-bound integers to uint8 arrays.
    
    This reproduces the bug where assigning values like 256, 257, 258 to uint8 arrays
    would produce deprecation warnings in NumPy 1.24+.
    """
    # Create a colormap with default N=256
    cmap = plt.get_cmap()
    
    # Test with empty uint8 array - this should not produce warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This is the exact case from the bug report
        result = cmap(np.empty((0, ), dtype=np.uint8))
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, np.VisibleDeprecationWarning) 
                               or "out-of-bound" in str(warning.message)]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we got the expected result
        assert result.shape == (0, 4), f"Expected shape (0, 4), got {result.shape}"


def test_colormap_with_out_of_bounds_values():
    """
    Test colormap behavior with values that would trigger out-of-bound assignments.
    """
    # Create a colormap with default N=256
    cmap = plt.get_cmap()
    
    # Test with uint8 array that contains values that would be out of bounds
    # when converted to indices, specifically testing the assignment of 
    # _i_over, _i_under, _i_bad values
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Create array with some values that would trigger boundary conditions
        # This should not produce warnings even though it involves boundary assignments
        test_values = np.array([0, 1, 255], dtype=np.uint8)
        result = cmap(test_values)
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, np.VisibleDeprecationWarning) 
                               or "out-of-bound" in str(warning.message)]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we got the expected result
        assert result.shape == (3, 4), f"Expected shape (3, 4), got {result.shape}"


def test_colormap_float_deprecation_warnings():
    """
    Test that colormap __call__ does not produce NumPy 1.24 deprecation warnings
    when working with float arrays that trigger the fixed code path.
    
    This specifically tests the code path where xa.dtype.kind == "f" is true,
    which is the path that was modified in the pull request.
    """
    # Create a colormap with default N=256
    cmap = plt.get_cmap()
    
    # Test with float array - this should trigger the float processing path
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Create float array that will trigger the float processing path
        # and potentially cause out-of-bound assignments
        test_values = np.array([0.0, 0.5, 1.0], dtype=np.float64)
        result = cmap(test_values)
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, np.VisibleDeprecationWarning) 
                               or "out-of-bound" in str(warning.message)]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we got the expected result
        assert result.shape == (3, 4), f"Expected shape (3, 4), got {result.shape}"


def test_colormap_edge_case_deprecation_warnings():
    """
    Test edge case that specifically triggers the assignment of _i_over, _i_under, _i_bad
    values to arrays, which was the source of the NumPy deprecation warnings.
    """
    # Create a colormap with default N=256
    cmap = plt.get_cmap()
    
    # Test with values that would be out of bounds and trigger the assignment
    # of _i_over, _i_under, _i_bad values
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Create array with values that will be clipped to boundaries
        # This should not produce warnings even though it involves boundary assignments
        test_values = np.array([-1.0, 1.1, np.nan], dtype=np.float64)
        result = cmap(test_values)
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, np.VisibleDeprecationWarning) 
                               or "out-of-bound" in str(warning.message)]
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )
        
        # Verify we got the expected result
        assert result.shape == (3, 4), f"Expected shape (3, 4), got {result.shape}"