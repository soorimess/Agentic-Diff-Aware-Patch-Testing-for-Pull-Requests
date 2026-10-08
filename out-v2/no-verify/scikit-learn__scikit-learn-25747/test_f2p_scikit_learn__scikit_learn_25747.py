"""Test for FeatureUnion with pandas transform output and custom transformer.

This test reproduces the bug where FeatureUnion fails when using pandas transform
output with a custom transformer that returns a pandas DataFrame with a different
index than the original input.
"""

import pandas as pd
import pytest
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union


class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None, **kwargs):
        return self

    def transform(self, X, y=None):
        # This transformer returns a DataFrame with a different index than input
        return X["value"].groupby(X["date"]).sum()


def test_feature_union_pandas_transform_output():
    """Test that FeatureUnion works with pandas transform output and custom transformer."""
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # This should work with default transform output
    set_config(transform_output="default")
    result_default = make_union(MyTransformer()).fit_transform(data)
    
    # This should also work but previously failed with ValueError
    set_config(transform_output="pandas")
    result_pandas = make_union(MyTransformer()).fit_transform(data)
    
    # Both should produce valid results
    assert result_default is not None
    assert result_pandas is not None


def test_feature_union_pandas_transform_output_with_multiple_transformers():
    """Test FeatureUnion with multiple transformers using pandas transform output."""
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # Create two transformers that return DataFrames with different indices
    class Transformer1(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            return X["value"].groupby(X["date"]).sum()

    class Transformer2(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            return X["value"].groupby(X["date"]).mean()

    # Test with pandas transform output
    set_config(transform_output="pandas")
    
    # This should not raise ValueError: Length mismatch
    union = make_union(Transformer1(), Transformer2())
    result = union.fit_transform(data)
    
    assert result is not None
    assert isinstance(result, pd.DataFrame)