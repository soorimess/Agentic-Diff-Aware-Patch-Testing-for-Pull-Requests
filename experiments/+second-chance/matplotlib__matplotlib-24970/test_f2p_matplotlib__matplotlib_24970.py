"""
Regression test for the NumPy 1.24 deprecation warnings bug.

This test ensures that calls to colormap.__call__ with empty uint8 arrays
do not produce NumPy deprecation warnings about out-of-bound integer conversions.
"""
import numpy as np
import warnings
from matplotlib import pyplot as plt


def test_colormap_empty_uint8_no_warnings():
    """Test that colormap.__call__ with empty uint8 array does not raise warnings."""
    # The bug was triggered by calling get_cmap()(np.empty((0, ), dtype=np.uint8))
    # This should not produce any NumPy deprecation warnings about out-of-bound conversions
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        cmap = plt.get_cmap()
        result = cmap(np.empty((0, ), dtype=np.uint8))
        
        # Check that no deprecation warnings about "out-of-bound" conversions were raised
        out_of_bound_warnings = [
            warning for warning in w 
            if 'out-of-bound' in str(warning.message)
        ]
        
        assert len(out_of_bound_warnings) == 0, (
            f"Unexpected NumPy out-of-bound warnings found: {[str(w.message) for w in out_of_bound_warnings]}"
        )


if __name__ == "__main__":
    # Run the test to verify it fails before fix (as expected for regression test)
    test_colormap_empty_uint8_no_warnings()
    print("Test completed - if we get here without assertion error, test passes")