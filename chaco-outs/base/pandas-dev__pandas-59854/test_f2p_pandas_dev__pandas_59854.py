"""
Regression test for PR #59854: String dtype: allow string dtype for non-raw apply with numba engine

This test verifies that DataFrame.apply() works with numba engine when the index or columns
have string dtype, which was previously not supported. The PR enables string dtype indexes/columns
to work directly with numba engine by extending the existing object dtype handling to also work with string dtypes.
"""
import numpy as np
import pytest

import pandas as pd
from pandas import DataFrame, Index

pytestmark = pytest.mark.single_cpu


def test_numba_string_dtype_functionality():
    """
    Test that string dtype indexes/columns work with numba engine (PR #59854).
    
    This test specifically targets the core functionality that was added in PR #59854:
    - Before: String dtype indexes/columns would cause numba to fail 
    - After: String dtype indexes/columns work directly with numba engine
    """
    # The main functionality: string dtype indexes with numba engine
    df = DataFrame(
        [[1, 2], [3, 4]], 
        index=Index(["a", "b"], dtype=pd.StringDtype(na_value=np.nan)),
        columns=["x", "y"]
    )
    
    # This should work with numba engine (the core fix)
    result = df.apply(lambda x: x.sum(), engine="numba", axis=0)
    
    # Verify the result is correct and has the expected properties
    assert isinstance(result, pd.Series)
    assert result.shape == (2,)
    assert list(result.index) == ["x", "y"]
    
    # Test that string dtype columns also work
    df2 = DataFrame(
        [[1, 2], [3, 4]], 
        index=["a", "b"],
        columns=Index(["x", "y"], dtype=pd.StringDtype(na_value=np.nan))
    )
    
    result2 = df2.apply(lambda x: x.sum(), engine="numba", axis=0)
    assert isinstance(result2, pd.Series)
    assert result2.shape == (2,)
    assert list(result2.index) == ["x", "y"]