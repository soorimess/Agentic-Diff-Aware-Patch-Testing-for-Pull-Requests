"""
Regression test for NumPy 1.24 deprecation warnings issue.
Tests the specific case from the bug report that was causing deprecation warnings.
"""
import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_empty_uint8_no_deprecation_warnings():
    """Test that plt.get_cmap()(np.empty((0, ), dtype=np.uint8)) produces no deprecation warnings.
    
    This test ensures that the fix for NumPy 1.24 deprecation warnings works properly.
    The specific case from the bug report: when an empty uint8 array is passed to a 
    colormap's __call__ method, it should not produce warnings about out-of-bound 
    integer conversions.
    """
    # This is the exact reproduction case from the bug report
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Filter for deprecation warnings - should be zero in fixed version
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        
        # The fix ensures that for this specific case, no deprecation warnings are emitted
        assert len(deprecation_warnings) == 0, (
            f"Expected no deprecation warnings, but got {len(deprecation_warnings)} warnings:\n"
            f"{[str(warn.message)[:100] + '...' if len(str(warn.message)) > 100 else str(warn.message) for warn in deprecation_warnings]}"
        )


if __name__ == "__main__":
    test_colormap_empty_uint8_no_deprecation_warnings()
    print("Test passed - no deprecation warnings for empty uint8 array case")