"""
Tests for the NumPy 1.24 deprecation warnings in matplotlib colormap __call__ method.

The issue: When accessing colormap values where _i_over, _i_under, _i_bad are set 
to high values (N+1, N, N+2), and numpy arrays use uint8 dtype, assignments like
xa[xa > self.N - 1] = self._i_over trigger overflow warnings because 257 doesn't 
fit in uint8.

This happens in the specific circumstance where _i_over, _i_under, _i_bad values
are stored into uint8 arrays where some values exceed the uint8 range.
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt


def test_colormap_no_deprecation_warnings_for_empty_uint8():
    """
    Test the specific case from the bug report that generates deprecation warnings.
    Before the fix: This would cause 3 deprecation warnings 
    After the fix: No warnings should occur
    
    The problem: This specific case (empty uint8 array) exposes issues in how
    the colormap __call__ method assigns out-of-range integer values to signed
    integer arrays that get promoted to uint8.
    """
    # Capture all warnings 
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This specific scenario causes the deprecation warnings
        # np.empty((0, ), dtype=np.uint8) creates an empty array with uint8 dtype
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check for deprecation warnings specifically
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        
        # Before the fix: we would see deprecation warnings
        # After the fix: there should be no deprecation warnings
        assert len(deprecation_warnings) == 0, \
            f"Expected no deprecation warnings, but got {len(deprecation_warnings)}: {[str(w.message) for w in deprecation_warnings]}"


if __name__ == "__main__":
    test_colormap_no_deprecation_warnings_for_empty_uint8()
    print("Test passed: No deprecation warnings for empty uint8 array")