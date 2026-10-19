"""
Regression test for PR #60295: TST (string dtype): resolve xfails for frame fillna and replace tests + fix bug in replace for string

This test ensures that the fix for broadcasting issues with 1D conditions in 2D blocks
for string dtypes works correctly.
"""
import numpy as np

import pandas as pd
from pandas import DataFrame


def test_string_dtype_where_broadcasting():
    """
    Test that where operations work with 1D conditions on 2D string blocks.
    
    This test specifically addresses the fix for PR #60295 which resolves:
    - Broadcasting issues with 1D conditions in 2D blocks for string dtypes
    - The error "Array conditional must be same shape as self" 
    """
    # Create DataFrame with string dtype - this creates 2D block structure
    df = DataFrame({"A": ["a", "b", "c"], "B": ["x", "y", "z"]}, dtype="string")
    
    # Create 1D condition array - this is the problematic case that needs broadcasting
    condition = np.array([True, False, True])
    
    # This operation should work correctly after the fix is applied
    # It currently fails in the old code with "Array conditional must be same shape as self"
    # The fix in blocks.py handles 1D conditions properly for 2D string blocks
    result = df.where(condition, "replaced")
    
    # If we get here, the fix is working - verify basic structure
    assert result.shape == (3, 2)
    assert str(result.dtypes["A"]) == "string"
    assert str(result.dtypes["B"]) == "string"
    
    # Verify the specific values that would be expected after the fix
    # Row 0: keep "a", "x" 
    # Row 1: replace with "replaced", "replaced"
    # Row 2: keep "c", "z"
    assert list(result["A"]) == ["a", "replaced", "c"]
    assert list(result["B"]) == ["x", "replaced", "z"]