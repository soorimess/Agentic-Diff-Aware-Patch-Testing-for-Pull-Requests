"""
Test for matplotlib bug #24970: NumPy 1.24 deprecation warnings in colormap processing.

This test ensures that colormap processing doesn't emit deprecation warnings
when handling out-of-bound values, which was introduced in NumPy 1.24.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_no_deprecation_warnings():
    """Test that colormap processing doesn't emit NumPy deprecation warnings."""
    # Test the exact case from the bug report
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        # Check no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, (np.VisibleDeprecationWarning, FutureWarning)) or 
                                  "deprecation" in str(warning.category).lower()]
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(w.message) for w in deprecation_warnings]}"
    
    # Test with values that could cause out-of-bound issues
    test_values = np.array([256, 257, 258], dtype=np.float64)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = plt.get_cmap()(test_values)
        # Check no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, (np.VisibleDeprecationWarning, FutureWarning)) or 
                                  "deprecation" in str(warning.category).lower()]
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(w.message) for w in deprecation_warnings]}"


def test_colormap_correct_behavior():
    """Test that colormap processing still produces correct results."""
    cmap = plt.get_cmap()
    
    # Test basic functionality still works
    result = cmap(0.5)
    assert len(result) == 4  # RGBA values
    
    # Test with array input
    values = np.array([0.0, 0.5, 1.0])
    result = cmap(values)
    assert len(result) == 3
    assert len(result[0]) == 4
    
    # Test with out-of-bound values (should be clipped)
    values = np.array([-1, 2, 3])
    result = cmap(values)
    assert len(result) == 3
    assert len(result[0]) == 4