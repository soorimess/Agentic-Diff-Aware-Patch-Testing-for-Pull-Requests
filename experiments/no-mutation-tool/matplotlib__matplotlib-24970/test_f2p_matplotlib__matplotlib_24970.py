"""
Regression test for NumPy 1.24 deprecation warnings in colormap processing.

This test ensures that colormap's __call__ method doesn't generate
NumPy 1.24 deprecation warnings when handling out-of-bound integer values
"""
import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_no_numpy_deprecation_warnings():
    """Test that colormap processing doesn't produce NumPy 1.24 deprecation warnings."""
    # Create a colormap 
    cmap = plt.get_cmap()
    
    # Test the exact case from the bug report that triggers the warning
    data = np.empty((0,), dtype=np.uint8)
    
    # Capture warnings - specifically look for NumPy out-of-bound warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(data)
        
        # Check that no NumPy deprecation warnings were raised
        numpy_warnings = [
            warning for warning in w 
            if (issubclass(warning.category, (FutureWarning, DeprecationWarning, np.VisibleDeprecationWarning)) 
                and 'out-of-bound' in str(warning.message).lower())
        ]
        assert len(numpy_warnings) == 0, f"Found {len(numpy_warnings)} NumPy deprecation warnings: {[str(warn.message) for warn in numpy_warnings]}"


def test_colormap_special_index_assignments():
    """Test that special index value assignments don't generate warnings."""
    cmap = plt.get_cmap()
    
    # Test cases that should trigger the special index assignments:
    # _i_under = 256, _i_over = 257, _i_bad = 258
    
    test_cases = [
        # Test negative values that trigger _i_under assignment
        np.array([-1.0], dtype=np.float64),
        # Test very large values that trigger _i_over assignment
        np.array([256.0], dtype=np.float64),  # Would exceed N-1 = 255 
        # Test NaN values that trigger _i_bad assignment
        np.array([np.nan], dtype=np.float64),
    ]
    
    for i, test_data in enumerate(test_cases):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = cmap(test_data)
            
            # Check that no NumPy deprecation warnings were raised
            numpy_warnings = [
                warning for warning in w 
                if (issubclass(warning.category, (FutureWarning, DeprecationWarning, np.VisibleDeprecationWarning)) 
                    and 'out-of-bound' in str(warning.message).lower())
            ]
            assert len(numpy_warnings) == 0, f"Test case {i} found {len(numpy_warnings)} NumPy warnings: {[str(warn.message) for warn in numpy_warnings]}"


if __name__ == "__main__":
    test_colormap_no_numpy_deprecation_warnings()
    test_colormap_special_index_assignments()
    print("All tests passed!")