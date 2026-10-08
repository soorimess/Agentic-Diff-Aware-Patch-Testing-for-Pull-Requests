"""Test for regression of FeatureUnion with pandas transform output.

This test reproduces the bug where FeatureUnion fails when using pandas
transform output with a transformer that returns a DataFrame with different
shape than the input.
"""

import pandas as pd
import pytest
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union


class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame, y=None, **kwargs):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        return X["value"].groupby(X["date"]).sum()


def test_feature_union_pandas_transform_output():
    """Test that FeatureUnion works with pandas transform output and 
    transformers that return DataFrames with different shapes."""
    
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # This should work (default transform output)
    set_config(transform_output="default")
    result_default = make_union(MyTransformer()).fit_transform(data)
    
    # This should also work but previously failed with ValueError
    set_config(transform_output="pandas")
    result_pandas = make_union(MyTransformer()).fit_transform(data)
    
    # Both should not raise an error and should produce valid results
    assert result_default is not None
    assert result_pandas is not None
    
    # The key test: no ValueError should be raised
    # The actual shapes may differ due to aggregation, but the important thing is
    # that it doesn't crash with a length mismatch error


def test_feature_union_with_multiple_transformers():
    """Test FeatureUnion with multiple transformers using pandas output."""
    
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # Create transformers that return different shaped DataFrames
    class Transformer1(BaseEstimator, TransformerMixin):
        def fit(self, X: pd.DataFrame, y=None, **kwargs):
            return self

        def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
            return X[["value"]].copy()  # Same shape

    class Transformer2(BaseEstimator, TransformerMixin):
        def fit(self, X: pd.DataFrame, y=None, **kwargs):
            return self

        def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
            return X["value"].groupby(X["date"]).sum().to_frame()  # Different shape

    # Test with pandas output
    set_config(transform_output="pandas")
    
    # This should not raise an error
    result = make_union(Transformer1(), Transformer2()).fit_transform(data)
    
    # Result should be a DataFrame
    assert isinstance(result, pd.DataFrame)