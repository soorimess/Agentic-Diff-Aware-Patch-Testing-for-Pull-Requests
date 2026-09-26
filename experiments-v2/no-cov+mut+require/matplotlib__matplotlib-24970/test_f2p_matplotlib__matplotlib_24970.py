import numpy as np
import matplotlib.pyplot as plt
import warnings

def test_colormap_empty_uint8_no_warnings():
    """
    Test that calling a colormap with empty uint8 array produces no deprecation warnings.
    
    This is a regression test for the NumPy 1.24 deprecation warnings issue.
    The bug occurred when np.errstate(invalid="ignore") was moved outside the 
    floating-point check, causing uint8 arrays to trigger deprecation warnings
    during astype(int) conversion.
    """
    # Capture all warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This is the exact reproduction case from the bug report
        result = plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
        
        # Check that no deprecation warnings were raised
        deprecation_warnings = [warning for warning in w 
                               if issubclass(warning.category, (np.VisibleDeprecationWarning, DeprecationWarning))]
        
        assert len(deprecation_warnings) == 0, (
            f"Expected no deprecation warnings, but got {len(deprecation_warnings)}: "
            f"{[str(warn.message) for warn in deprecation_warnings]}"
        )