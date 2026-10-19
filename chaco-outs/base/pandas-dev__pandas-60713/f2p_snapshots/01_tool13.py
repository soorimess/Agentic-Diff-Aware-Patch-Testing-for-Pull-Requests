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
        
        # This should raise TypeError
        with pytest.raises(TypeError, match="Cannot change data-type for string array"):
            arr.view(dtype=np.dtype("int64"))
    
    def test_view_dtype_none_works(self):
        """Test that view() with dtype=None works as expected."""
        arr = StringArray._from_sequence(["a", "b", "c"])
        
        # This should work (call super().view(dtype=None))
        result = arr.view(dtype=None)
        # Should return the same array or a view of it
        assert isinstance(result, StringArray)
        assert len(result) == 3