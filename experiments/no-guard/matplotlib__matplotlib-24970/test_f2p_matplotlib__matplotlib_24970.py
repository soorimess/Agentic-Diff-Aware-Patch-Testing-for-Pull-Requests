import numpy as np
import matplotlib.pyplot as plt
import warnings


def test_colormap_empty_uint8_no_deprecation_warnings():
    """
    Test that colormap.__call__ on empty uint8 array does not produce NumPy 1.24 deprecation warnings.
    
    This test reproduces the exact bug case from the issue report where:
    - Empty uint8 array is passed to a colormap 
    - Assignment of out-of-bound values like _i_over=257, _i_under=256, _i_bad=258
    - to uint8 arrays causes numpy warnings about out-of-bound integer conversion
    
    The fix moved np.errstate(invalid="ignore") to wrap only the final astype(int) call
    instead of all range handling operations.
    """
    # Test case exactly as provided in the bug report
    cmap = plt.get_cmap()
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(np.empty((0,), dtype=np.uint8))
        # Should produce no NumPy deprecation warnings for out-of-bound integer assignments
        deprecation_warnings = []
        for warning in w:
            if issubclass(warning.category, DeprecationWarning):
                message = str(warning.message)
                if "out-of-bound Python integers" in message and "uint8" in message:
                    deprecation_warnings.append(message)
                    
        assert len(deprecation_warnings) == 0, (
            f"Expected no NumPy uint8 out-of-bound integer warnings, "
            f"but got {len(deprecation_warnings)}: {deprecation_warnings}"
        )
        # Overall we expect no warnings at all
        assert len(w) == 0, f"Expected no warnings, got {len(w)} warnings: {[str(warn.message) for warn in w]}"


def test_colormap_uint8_range_assignment_behavior():
    """
    Test that range assignment operations don't produce deprecation warnings.
    
    Tests specifically for the integer assignment that happens after the reordering.
    When arrays get values that exceed their dtype limits, this should not warn
    with the proper error handling context manager around only the casting.
    """
    # Test with values that go through under/over range handling
    cmap = plt.get_cmap('viridis')  # N=256 by default
    
    # Test values that cause range code paths to execute
    test_values = np.array([-0.5, 0.0, 0.5, 1.0, 1.5]) 
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = cmap(test_values)
        # The behavior to ensure: warnings should not include NumPy out-of-bound issues
        deprecation_warnings = []
        for warning in w:
            if issubclass(warning.category, DeprecationWarning):
                message = str(warning.message)
                if "out-of-bound Python integers" in message and "uint8" in message:
                    deprecation_warnings.append(message)
                    
        assert len(deprecation_warnings) == 0, (
            f"Expected no NumPy out-of-bound integer warnings, "
            f"but got {len(deprecation_warnings)}: {deprecation_warnings}"
        )