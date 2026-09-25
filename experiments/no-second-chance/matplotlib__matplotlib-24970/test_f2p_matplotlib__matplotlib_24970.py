import numpy as np
import matplotlib.pyplot as plt
import warnings

def test_numpy_124_deprecation_warnings_empty_uint8():
    """Test for NumPy 1.24 deprecation warnings with empty uint8 array (original bug report case).
    
    This addresses the specific case in the bug report where:
    plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
    was causing deprecation warnings about out-of-bound integer assignments.
    """
    # This is the exact case from the bug report that reproduces the warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check that no deprecation warnings were raised - this is the issue we're fixing
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(w.message) for w in deprecation_warnings]}"

def test_colormap_no_deprecation_warnings_with_range_values():
    """Test that colormap processing with values in proper range also doesn't produce warnings."""
    # Test with actual values that will test the full colormap processing
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Simple array of values in the valid range
        test_array = np.array([0.0, 0.5, 1.0], dtype=np.float64)
        result = plt.get_cmap()(test_array)
        
        # Check no deprecation warnings 
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(w.message) for w in deprecation_warnings]}"