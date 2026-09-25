"""
Test for matplotlib bug: NumPy 1.24 deprecation warnings
This specifically tests the change in behavior for how 
np.errstate is used during colormap processing which affects
NumPy deprecation warnings in newer NumPy versions.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_no_deprecation_warnings_for_empty_uint8_array():
    """Test that calling colormap on empty uint8 array doesn't cause deprecation warnings."""
    # This exact case from the bug report should not produce warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Exact reproduction case from bug report
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Count all NumPy-specific deprecation warnings
        deprecation_warnings = []
        for warning in w:
            if ('deprecat' in str(warning.category).lower() or 
                'out-of-bound' in str(warning.message).lower()):
                deprecation_warnings.append(warning)
        
        # In the buggy version, we'd see deprecation warnings about
        # "NumPy will stop allowing conversion of out-of-bound Python integers"
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings "
            f"when calling colormap on empty uint8 array: "
            f"{[str(w.message) for w in deprecation_warnings]}"
        )


def test_colormap_handles_float_overflow_properly():
    """Test that colormap handles large float values correctly without warnings."""
    cmap = plt.get_cmap()
    
    # Test case that could cause issues with integer overflow during indexing
    # Triggering bounds checking that was problematic
    test_data = np.array([2.0, 3.0, 10.0])  # Out of [0,1] range
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        result = cmap(test_data)
        
        # Check for NumPy deprecation warnings specifically
        deprecation_warnings = []
        for warning in w:
            if 'deprecat' in str(warning.category).lower():
                deprecation_warnings.append(warning)
        
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} NumPy deprecation warnings "
            f"during handling of out-of-bounds float values: "
            f"{[str(w.message) for w in deprecation_warnings]}"
        )