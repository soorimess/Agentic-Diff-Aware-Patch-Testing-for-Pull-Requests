"""
Regression test for FeatureUnion with pandas transform output and DataFrame return.

This test ensures that FeatureUnion works correctly when:
1. Using transform_output="pandas" configuration
2. A transformer returns a pandas DataFrame with a different shape/index than input
3. The result should not raise a ValueError about index length mismatch
"""
import pytest
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union


class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # Return a DataFrame with different shape than input (group by date)
        return X["value"].groupby(X["date"]).sum()


def test_feature_union_pandas_transform_output_dataframe_return():
    """Test that FeatureUnion works with pandas transform output when transformer returns DataFrame."""
    # Create test data with 96 rows (5 days * 24 hours)
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    # Test with default transform output (should work)
    set_config(transform_output="default")
    result_default = make_union(MyTransformer()).fit_transform(data)
    expected_shape_default = (4,)  # 4 unique dates
    assert result_default.shape == expected_shape_default

    # Test with pandas transform output (this was broken before the fix)
    set_config(transform_output="pandas")
    result_pandas = make_union(MyTransformer()).fit_transform(data)
    
    # The result should be a DataFrame with the correct shape and index
    assert isinstance(result_pandas, pd.DataFrame)
    # Should have 4 rows (one per unique date) 
    assert len(result_pandas) == 4
    # Should have the correct index (the unique dates)
    expected_index = sorted(data["date"].unique())
    assert list(result_pandas.index) == expected_index


def test_feature_union_pandas_transform_output_dataframe_return_multiple_transformers():
    """Test that FeatureUnion works with multiple transformers returning DataFrames."""
    # Create test data with 96 rows (5 days * 24 hours)
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    class Transformer1(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self

        def transform(self, X, y=None):
            return X["value"].groupby(X["date"]).sum()

    class Transformer2(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self

        def transform(self, X, y=None):
            return X["value"].groupby(X["date"]).count()

    # Test with pandas transform output
    set_config(transform_output="pandas")
    result = make_union(Transformer1(), Transformer2()).fit_transform(data)
    
    # The result should be a DataFrame with the correct shape and index
    assert isinstance(result, pd.DataFrame)
    # Should have 4 rows (one per unique date) 
    assert len(result) == 4
    # Should have 2 columns (one for each transformer)
    assert len(result.columns) == 2