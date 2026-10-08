"""Test for FeatureUnion with pandas transform output.

This test reproduces the bug where FeatureUnion fails when using pandas
transform output and a transformer that returns a DataFrame from its transform
method.
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
        return X["value"].groupby(X["date"]).sum()


def test_feature_union_pandas_transform_output():
    """Test that FeatureUnion works with pandas transform output."""
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    # This should work with default transform output
    set_config(transform_output="default")
    result_default = make_union(MyTransformer()).fit_transform(data)
    
    # This should also work but currently fails with the bug
    set_config(transform_output="pandas")
    result_pandas = make_union(MyTransformer()).fit_transform(data)
    
    # Both should produce results
    assert result_default is not None
    assert result_pandas is not None


def test_feature_union_pandas_transform_output_with_index_mismatch():
    """Test the specific case that causes index length mismatch."""
    # Create test data with specific structure
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    # Set to pandas output mode
    set_config(transform_output="pandas")
    
    # This should not raise a ValueError about length mismatch
    union = make_union(MyTransformer())
    result = union.fit_transform(data)
    
    # The result should be a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # The result should have the expected shape
    # Original data has 96 rows (4 days * 24 hours)
    # After groupby and sum, we should have 4 rows (one per date)
    assert result.shape[0] == 4  # 4 unique dates
    assert result.shape[1] == 1  # 1 column (the sum)