import numpy as np
import warnings
import matplotlib.pyplot as plt
import pytest


def test_colormap_no_deprecation_warnings():
    """
    Test that colormap calls do not generate NumPy 1.24+ deprecation warnings
    about conversion of out-of-bound Python integers to integer arrays.
    
    This test ensures that calling a colormap with certain inputs does not
    trigger deprecation warnings that were introduced in NumPy 1.24.
    """
    # Test case from the bug report - empty uint8 array
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should not generate deprecation warnings
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, DeprecationWarning)]
        
        # There should be no deprecation warnings
        assert len(deprecation_warnings) == 0, (
            f"Found {len(deprecation_warnings)} deprecation warnings: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )