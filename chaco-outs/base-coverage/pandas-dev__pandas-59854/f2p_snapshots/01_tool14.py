"""
Regression test for PR #59854: String dtype: allow string dtype for non-raw apply with numba engine

This test ensures that apply operations with numba engine work correctly when
the DataFrame has string dtype indexes/columns.
"""
import numpy as np
import pytest

import pandas as pd
from pandas import DataFrame


class TestNumbaStringDtypeApply:
    def test_apply_string_columns_with_numba_engine(self):
        """Test that apply works with string dtype columns using numba engine."""
        # Create DataFrame with string dtype columns
        df = DataFrame(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            columns=pd.Index(["A", "B", "C"], dtype="string")
        )
        
        # This should work with the fix (before it would fail with AttributeError or similar)
        # The key test is that it doesn't raise an exception
        result = df.apply(lambda x: x.sum(), axis=1, engine="numba")
        
        # Verify the result
        expected = pd.Series([6, 15, 24], dtype="int64")
        pd.testing.assert_series_equal(result, expected)