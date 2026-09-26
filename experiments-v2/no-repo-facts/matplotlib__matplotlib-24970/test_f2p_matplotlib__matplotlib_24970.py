import numpy as np
import matplotlib.pyplot as plt
import warnings

def test_numpy_deprecation_warnings():
    """Test for NumPy 1.24 deprecation warnings in colormap processing."""
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This is the reproduction case from the bug report
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check if any deprecation warnings were raised
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        
        # The bug is that we get deprecation warnings about out-of-bound integer conversion
        # These should not happen with the fix
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"

def test_colormap_with_float_values():
    """Test colormap processing with float values that trigger the problematic conversion."""
    
    # Create a colormap
    cmap = plt.get_cmap()
    
    # Test with values that when multiplied by N (e.g., 256) would result in 
    # values that cause out-of-bound integer conversion warnings in NumPy 1.24+
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Test with float values that when multiplied by 256 become > 255
        # This is the key case that triggers the issue
        test_values = np.array([1.001, 1.002, 1.003])  # These when multiplied by 256 > 255
        result = cmap(test_values)
        
        # Check if any deprecation warnings were raised
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        
        # The fix should prevent these warnings
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
        
        # Verify that we get reasonable results
        assert result.shape == (3, 4), f"Expected shape (3, 4), got {result.shape}"

def test_colormap_with_integer_values():
    """Test colormap processing with integer values that might cause issues."""
    
    # Create a colormap
    cmap = plt.get_cmap()
    
    # Test with integer values that might be out of bounds for typical colormap
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # These values should not cause deprecation warnings
        test_values = np.array([256, 257, 258])  # Values that would be out of range for 256-color cmap
        result = cmap(test_values)
        
        # Check if any deprecation warnings were raised
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        
        # The fix should prevent these warnings
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
        
        # Verify that we get reasonable results
        assert result.shape == (3, 4), f"Expected shape (3, 4), got {result.shape}"

def test_colormap_with_mixed_values():
    """Test colormap processing with mixed value types."""
    
    # Create a colormap
    cmap = plt.get_cmap()
    
    # Test with mixed values that could trigger the conversion path
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Mix of values that when processed could cause issues
        test_values = np.array([0.0, 0.5, 1.0, 256.0, 257.0])  # Mixed valid and out-of-range
        result = cmap(test_values)
        
        # Check if any deprecation warnings were raised
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
        
        # The fix should prevent these warnings
        assert len(deprecation_warnings) == 0, f"Got {len(deprecation_warnings)} deprecation warnings: {[str(warn.message) for warn in deprecation_warnings]}"
        
        # Verify that we get reasonable results
        assert result.shape == (5, 4), f"Expected shape (5, 4), got {result.shape}"

if __name__ == "__main__":
    test_numpy_deprecation_warnings()
    test_colormap_with_float_values()
    test_colormap_with_integer_values()
    test_colormap_with_mixed_values()
    print("All tests passed!")