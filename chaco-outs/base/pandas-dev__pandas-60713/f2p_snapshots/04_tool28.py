"""
Regression test for pull request #60713
Test that BaseStringArray.view() raises TypeError when dtype is not None.
"""
import numpy as np
import pytest

import pandas as pd
from pandas import StringDtype
from pandas.core.arrays import StringArray


class TestStringArrayView:
    def test_view_dtype_not_none_raises(self):
        """Test that view() raises TypeError when dtype is not None."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should raise TypeError with specific message
        with pytest.raises(TypeError, match="Cannot change data-type for string array."):
            arr.view(dtype=np.dtype("int64"))
    
    def test_view_dtype_none_works(self):
        """Test that view() with dtype=None works as expected."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should work (call super().view(dtype=None))
        result = arr.view(dtype=None)
        # Should return the same array or a view of it
        assert isinstance(result, StringArray)
        assert len(result) == 3
    
    def test_view_no_dtype_parameter(self):
        """Test that view() with no dtype parameter works as expected."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should work (call super().view(None))
        result = arr.view()
        # Should return the same array or a view of it
        assert isinstance(result, StringArray)
        assert len(result) == 3
        
    def test_view_different_dtype_raises(self):
        """Test that view() with different dtype raises TypeError."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # Test with different dtypes that should all raise TypeError
        for dtype in [np.dtype("float64"), np.dtype("int32"), object]:
            with pytest.raises(TypeError, match="Cannot change data-type for string array."):
                arr.view(dtype=dtype)
    
    def test_view_raises_error_not_from_numpy(self):
        """Test that the error comes from our implementation, not numpy."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should raise our specific TypeError, not a numpy one
        with pytest.raises(TypeError) as exc_info:
            arr.view(dtype=np.dtype("int64"))
        
        # Check that error message is from our code, not numpy
        assert "Cannot change data-type for string array" in str(exc_info.value)
        # Make sure it's NOT the numpy error message
        assert "Cannot change data-type for object array" not in str(exc_info.value)