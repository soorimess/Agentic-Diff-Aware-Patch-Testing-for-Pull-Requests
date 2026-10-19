"""
Regression test for pull request #60713
Test that BaseStringArray.view() raises TypeError when dtype is not None.
"""
import numpy as np
import pytest

import pandas as pd
from pandas.core.arrays import StringArray


class TestStringArrayView:
    def test_string_array_view_dtype_not_none_raises(self):
        # GH#60713
        # Test that BaseStringArray.view() raises TypeError when dtype is not None
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should raise TypeError
        with pytest.raises(TypeError, match="Cannot change data-type for string array"):
            arr.view(dtype=object)
            
    def test_string_array_view_dtype_none_works(self):
        # GH#60713
        # Test that BaseStringArray.view() with dtype=None works as expected
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should work fine (delegates to super().view)
        result = arr.view(dtype=None)
        # Should return the same array
        pd.testing.assert_extension_array_equal(result, arr)
        
    def test_string_array_view_behavior_with_different_dtypes(self):
        # GH#60713
        # Test that various dtype arguments properly raise TypeError
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # Test with different dtypes that should all raise TypeError
        for dtype_arg in [object, np.dtype('object'), 'object']:
            with pytest.raises(TypeError, match="Cannot change data-type for string array"):
                arr.view(dtype=dtype_arg)