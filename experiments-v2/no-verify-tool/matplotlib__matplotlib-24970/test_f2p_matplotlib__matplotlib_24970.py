import numpy as np
import warnings

from matplotlib import colormaps


def test_colormap_no_numpy_deprecation_warnings():
    """Test that colormap calls don't produce NumPy 1.24 deprecation warnings.
    
    This test ensures that when calling a colormap with values that would
    previously cause out-of-bound integer assignments, no deprecation warnings
    are raised. The issue was that assignments like xa[xa > self.N - 1] = self._i_over
    were not under np.errstate(invalid="ignore") context, causing NumPy 1.24+
    deprecation warnings.
    
    This test specifically targets the bug reported where assignment operations
    in colormap.__call__ were not properly suppressed under np.errstate, leading
    to deprecation warnings about out-of-bound integer conversions.
    """
    # Test the exact scenario that was causing warnings in NumPy 1.24+
    cmap = colormaps.get_cmap('viridis')
    
    # The bug occurs when calling colormap that triggers assignment operations
    # that should not produce deprecation warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This call exercises the problematic code path where assignments
        # like xa[xa > self.N - 1] = self._i_over were not under np.errstate
        result = cmap(np.empty((0, ), dtype=np.uint8))
        
        # Check that no NumPy deprecation warnings were raised
        deprecation_warnings = [
            warning for warning in w 
            if ("deprecation" in str(warning.category).lower() or
                "out-of-bound" in str(warning.message).lower())
        ]
        
        # In the buggy version, we would see deprecation warnings like:
        # "NumPy will stop allowing conversion of out-of-bound Python integers to integer arrays"
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} NumPy deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )