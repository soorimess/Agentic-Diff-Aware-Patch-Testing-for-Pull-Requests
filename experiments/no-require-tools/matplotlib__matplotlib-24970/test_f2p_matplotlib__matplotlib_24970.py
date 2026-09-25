"""
Test for regression of NumPy 1.24 deprecation warnings in color mapping.

This file tests that when color maps are applied to arrays containing
values that would trigger out-of-range assignment to _i_over/_i_under/_i_bad
constants, no deprecation warnings are raised (for NumPy 1.24+).
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
import pytest


def test_colormap_no_deprecation_warnings_for_out_of_range():
    """
    Test that applying a colormap to an array that triggers out-of-range 
    assignments doesn't produce NumPy deprecation warnings.
    
    The bug was that when assigning the out-of-range values such as 
    self._i_over = self.N + 1 (== 257) to arrays of uint8 type,  
    NumPy 1.24+ would emit deprecation warnings about integer overflow.
    """
    # Create a colormap
    cmap = plt.get_cmap()
    
    # Test with empty array - this is from the original bug report
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        result = cmap(np.empty((0, ), dtype=np.uint8))
        
        # Check no deprecation warnings about integer conversion
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        # Print warnings for debugging if needed
        if deprecation_warnings:
            print("Found deprecation warnings:")
            for warning in deprecation_warnings:
                print(f"  {warning.message}")
        
        # Should be no warnings
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings "
            f"when applying colormap to empty array: {[str(w.message) for w in deprecation_warnings]}"
        )
        
        # Also validate output shape
        assert result.shape == (0, 4)


def test_colormap_with_specific_boundary_values():
    """
    Test the specific problematic values mentioned in the original bug report.
    Check that assigning values like 256, 257, 258 (N, N+1, N+2) to arrays doesn't cause warnings.
    """
    cmap = plt.get_cmap()
    
    # Test with values that would be assigned to _i_over, _i_under, _i_bad 
    # (values N, N+1, N+2 for N=256)
    # However, the problem is not necessarily with these _exact_ values in our set up
    # but that the assignment pattern causes deprecation warnings when converted to arrays
    
    # Test with values that would trigger the assignment paths in the colormap code
    test_cases = [
        # Underflow case
        np.array([-1.0], dtype=np.float32),  
        # Overflow case  
        np.array([257.0], dtype=np.float32),
        np.array([np.nan], dtype=np.float32),   # Bad value case
        # Mixed case with problematic assignments
        np.array([-1.0, 257.0, np.nan], dtype=np.float32),
    ]
    
    for i, test_array in enumerate(test_cases):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = cmap(test_array)
            
            # Check specifically for the deprecation warnings that were reported
            deprecation_warnings = [warning for warning in w 
                                   if issubclass(warning.category, DeprecationWarning)]
            integer_overflow_warnings = [
                warning for warning in deprecation_warnings
                if "out-of-bound Python integers" in str(warning.message)
            ]
            
            assert len(integer_overflow_warnings) == 0, (
                f"Found integer overflow warnings for test case {i} with array {test_array}: "
                f"{[str(w.message) for w in integer_overflow_warnings]}"
            )
            
            # Verify output shape is correct
            expected_shape = (len(test_array), 4)
            assert result.shape == expected_shape, (
                f"Shape mismatch for array {test_array}: expected {expected_shape}, got {result.shape}"
            )


def test_colormap_original_bug_case():
    """
    Test the exact case reported in the bug report.
    """
    # This is the exact reproducer from the bug report
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check specifically for character replacements from NumPy deprecation message
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        integer_overflow_warnings = [
            warning for warning in deprecation_warnings
            if "out-of-bound Python integers" in str(warning.message)
        ]
        
        assert len(integer_overflow_warnings) == 0, (
            f"Found {len(integer_overflow_warnings)} integer overflow warnings "
            f"in original bug case: {[str(w.message) for w in integer_overflow_warnings]}"
        )
        
        assert result.shape == (0, 4)