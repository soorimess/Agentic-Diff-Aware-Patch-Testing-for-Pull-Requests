"""
Regression test for PR #58893: ENH: Add **kwargs to pivot_table to allow 
the specification of aggfunc keyword arguments
"""
import numpy as np
import pytest

import pandas as pd
from pandas import DataFrame
import pandas._testing as tm


class TestPivotTableKwargs:
    def test_pivot_table_accepts_aggfunc_kwargs(self):
        # Test that pivot_table now accepts kwargs that get passed to aggfunc
        # This should not raise TypeError about unexpected keyword arguments
        
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, np.nan],
            }
        )
        
        # This should work without raising TypeError
        # The kwargs (min_count) should be passed through to the aggfunc
        try:
            result = df.pivot_table(
                values="C", index="A", columns="B", aggfunc="sum", min_count=1
            )
            # If we get here without TypeError, the feature works
            assert isinstance(result, DataFrame)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                pytest.fail(f"pivot_table should accept kwargs but got: {e}")
            raise
    
    def test_pivot_table_function_kwargs(self):
        # Test that the function form also accepts kwargs
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, np.nan],
            }
        )
        
        # This should work without raising TypeError
        try:
            result = pd.pivot_table(
                df, values="C", index="A", columns="B", aggfunc="sum", min_count=1
            )
            # If we get here without TypeError, the feature works
            assert isinstance(result, DataFrame)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                pytest.fail(f"pivot_table should accept kwargs but got: {e}")
            raise

    def test_pivot_table_with_dict_aggfunc_and_kwargs(self):
        # Test that dict aggfunc works with kwargs
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
                "D": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0],
            }
        )
        
        # This should work without raising TypeError
        try:
            result = df.pivot_table(
                values=["C", "D"], 
                index="A", 
                columns="B", 
                aggfunc={"C": "sum", "D": "mean"}, 
                min_count=1
            )
            # If we get here without TypeError, the feature works
            assert isinstance(result, DataFrame)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                pytest.fail(f"pivot_table should accept kwargs with dict aggfunc but got: {e}")
            raise
            
    def test_pivot_table_with_custom_function_and_kwargs(self):
        # Test that custom aggfunc works with kwargs
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, np.nan],
            }
        )
        
        # Test with custom function and kwargs
        def sum_with_min_count(x, min_count=0):
            return x.sum(min_count=min_count)
            
        try:
            result = df.pivot_table(
                values="C", index="A", columns="B", aggfunc=sum_with_min_count, min_count=1
            )
            # If we get here without TypeError, the feature works
            assert isinstance(result, DataFrame)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                pytest.fail(f"pivot_table should accept kwargs with custom function but got: {e}")
            raise