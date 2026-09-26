import numpy as np
import matplotlib.pyplot as plt
import warnings
import pytest


def test_colormap_deprecation_warnings():
    """Test for NumPy 1.24 deprecation warnings in colormap processing.
    
    This test ensures that when colormap __call__ is used with values that
    would cause out-of-range assignments, no deprecation warnings are raised.
    """
    # Create a colormap with N=256 (standard colormap)
    cmap = plt.get_cmap()
    
    # Test case 1: Empty array (from the bug report)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(np.empty((0,), dtype=np.uint8))
        # Should not raise any deprecation warnings
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Unexpected deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
    
    # Test case 2: Values that would trigger out-of-range assignments
    # These should not produce deprecation warnings in the fixed version
    test_values = np.array([257, 256, 258], dtype=np.float64)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(test_values)
        # Should not raise any deprecation warnings
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Unexpected deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"


def test_colormap_edge_cases():
    """Test edge cases that would trigger the specific assignment operations."""
    cmap = plt.get_cmap()
    
    # Test with negative values that would be assigned to _i_under
    negative_values = np.array([-1, -2, -10], dtype=np.float64)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(negative_values)
        # Should not raise any deprecation warnings
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Unexpected deprecation warnings with negative values: {[str(warn.message) for warn in deprecation_warnings]}"
    
    # Test with values that exceed N-1 (would be assigned to _i_over)
    high_values = np.array([256, 257, 300], dtype=np.float64)  # N=256, so values >= 256 are over-range
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(high_values)
        # Should not raise any deprecation warnings
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Unexpected deprecation warnings with high values: {[str(warn.message) for warn in deprecation_warnings]}"
    
    # Test with NaN values that would be assigned to _i_bad
    nan_values = np.array([np.nan, np.nan], dtype=np.float64)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(nan_values)
        # Should not raise any deprecation warnings
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Unexpected deprecation warnings with NaN values: {[str(warn.message) for warn in deprecation_warnings]}"