"""
Regression test for PR #59141: REF: Make concat not stateful.
"""

import pytest
import pandas as pd
from pandas import DataFrame


def test_concat_sort_validation():
    """Test that concat properly validates sort parameter."""
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    
    # This should raise ValueError for non-boolean sort parameter
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        pd.concat([df1, df2], sort="invalid")


def test_concat_join_validation():
    """Test that concat properly validates join parameter."""
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    
    # This should raise ValueError for invalid join parameter
    with pytest.raises(ValueError, match="Only can inner.*outer.*union.*join.*other axis"):
        pd.concat([df1, df2], join="invalid")