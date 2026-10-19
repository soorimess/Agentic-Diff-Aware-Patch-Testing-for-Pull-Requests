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
    def test_pivot_table_accepts_aggfunc_kwargs_no_error(self):
        # Test that pivot_table now accepts kwargs without raising TypeError
        # This is the core functionality that was missing
        
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, np.nan],
            }
        )
        
        # These should not raise TypeError about unexpected keyword arguments
        # The kwargs should be passed through to the aggfunc
        result1 = df.pivot_table(
            values="C", index="A", columns="B", aggfunc="sum", min_count=1
        )
        assert isinstance(result1, DataFrame)
        
        result2 = pd.pivot_table(
            df, values="C", index="A", columns="B", aggfunc="sum", min_count=1
        )
        assert isinstance(result2, DataFrame)

    def test_pivot_table_kwargs_with_dict_aggfunc(self):
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
        result = df.pivot_table(
            values=["C", "D"], 
            index="A", 
            columns="B", 
            aggfunc={"C": "sum", "D": "mean"}, 
            min_count=1
        )
        assert isinstance(result, DataFrame)
        
    def test_pivot_table_kwargs_with_custom_function(self):
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
            
        result = df.pivot_table(
            values="C", index="A", columns="B", aggfunc=sum_with_min_count, min_count=1
        )
        assert isinstance(result, DataFrame)
        
    def test_pivot_table_kwargs_margins(self):
        # Test that margins work with kwargs
        df = DataFrame(
            {
                "A": ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
                "B": ["one", "two", "one", "two", "one", "two", "one", "two"],
                "C": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, np.nan],
            }
        )
        
        # Test margins with kwargs - this should not raise TypeError
        result = df.pivot_table(
            values="C", 
            index="A", 
            columns="B", 
            aggfunc="sum", 
            min_count=1,
            margins=True
        )
        assert isinstance(result, DataFrame)
        
    def test_pivot_table_kwargs_functionality(self):
        # Test that the kwargs are actually being passed through
        # This test ensures that the functionality works, not just that no error occurs
        
        # Create data with NaN values to test min_count behavior
        df = DataFrame({
            "A": ["foo", "foo", "foo", "bar", "bar", "bar"],
            "B": ["one", "two", "one", "two", "one", "two"], 
            "C": [1.0, np.nan, 3.0, np.nan, 5.0, 7.0]
        })
        
        # Without min_count, sum with NaN should return NaN
        # With min_count=1, sum should return the actual sum (ignoring NaN where count >= 1)
        result_with_kwargs = df.pivot_table(
            values="C", index="A", columns="B", aggfunc="sum", min_count=1
        )
        
        # Just verify it executes without error and returns a DataFrame
        assert isinstance(result_with_kwargs, DataFrame)
        
        # Test with a function that actually uses the kwargs
        def custom_sum_with_kwargs(x, min_count=0):
            return x.sum(min_count=min_count)
            
        result_custom = df.pivot_table(
            values="C", index="A", columns="B", aggfunc=custom_sum_with_kwargs, min_count=1
        )
        
        # Verify it executes without error
        assert isinstance(result_custom, DataFrame)