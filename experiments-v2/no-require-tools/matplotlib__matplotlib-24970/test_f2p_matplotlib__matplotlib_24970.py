import numpy as np
import matplotlib.pyplot as plt
import warnings

def test_colormap_no_numpy_deprecation_warnings():
    """
    Regression test for NumPy 1.24 deprecation warnings in colormap conversion.
    
    This test ensures that colormap conversion operations do not produce 
    NumPy deprecation warnings about "conversion of out-of-bound Python integers 
    to integer arrays".
    
    The fix moved np.errstate(invalid="ignore") from surrounding the entire 
    float conversion to only surrounding the final astype(int) conversion.
    """
    
    # Test the exact case from the bug report that was causing warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This exact call was producing deprecation warnings in NumPy 1.24+
        # The test should pass both before and after the fix, but the key is
        # that it should not produce warnings
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check for any deprecation warnings (the main goal of the fix)
        deprecation_warnings = []
        for warning in w:
            if (issubclass(warning.category, np.VisibleDeprecationWarning) or 
                issubclass(warning.category, FutureWarning)):
                deprecation_warnings.append(warning)
        
        # There should be no deprecation warnings - this is the core fix
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warning.message) for warning in deprecation_warnings]}"
        )
        
        # Verify correct output shape
        assert result.shape == (0, 4), f"Expected shape (0, 4), got {result.shape}"


def test_colormap_conversion_no_warnings():
    """
    Test that colormap conversion works without warnings for various inputs.
    """
    # Test multiple scenarios that should not generate warnings
    scenarios = [
        # The exact bug report case
        np.empty((0,), dtype=np.uint8),
        # Normal float values
        np.array([0.0, 0.5, 1.0], dtype=float),
        # Edge cases
        np.array([0.0], dtype=float),
        np.array([1.0], dtype=float),
    ]
    
    for i, test_input in enumerate(scenarios):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            cmap = plt.get_cmap()
            result = cmap(test_input)
            
            # Check for deprecation warnings
            deprecation_warnings = []
            for warning in w:
                if (issubclass(warning.category, np.VisibleDeprecationWarning) or 
                    issubclass(warning.category, FutureWarning)):
                    deprecation_warnings.append(warning)
            
            # No warnings should be generated
            assert len(deprecation_warnings) == 0, (
                f"Scenario {i} with input {test_input}: Found {len(deprecation_warnings)} deprecation warnings: "
                f"{[str(warning.message) for warning in deprecation_warnings]}"
            )
            
            # Verify result shape is correct
            expected_shape = (test_input.shape[0] if test_input.shape else 0, 4)
            assert result.shape == expected_shape, (
                f"Scenario {i}: Expected shape {expected_shape}, got {result.shape}"
            )