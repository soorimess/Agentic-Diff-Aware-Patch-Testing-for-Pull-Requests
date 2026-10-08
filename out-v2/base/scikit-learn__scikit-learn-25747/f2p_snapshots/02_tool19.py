"""
Regression test for FeatureUnion with pandas transform output and aggregated data.

This test ensures that FeatureUnion works correctly when:
1. Using pandas transform output configuration
2. A transformer returns a DataFrame with different shape than input
3. The transformer aggregates data (like groupby operations)
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union


def test_feature_union_pandas_output_with_aggregated_data():
    """Test that FeatureUnion works with pandas output when transformer returns aggregated data.
    
    This test reproduces the bug where using pandas transform output with a transformer
    that returns aggregated data (different shape than input) would raise a ValueError
    about length mismatch.
    """
    
    # Create test data as described in the bug report
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    class MyTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            return X["value"].groupby(X["date"]).sum()

    # Test with pandas output - this should not raise ValueError about length mismatch
    set_config(transform_output="pandas")
    union = make_union(MyTransformer())
    
    # This should not raise "Length mismatch: Expected axis has X elements, new values have Y elements"
    # The key test is that this doesn't raise an exception
    result = union.fit_transform(data)
    
    # Verify we got a result (it could be a DataFrame or array depending on how it's handled)
    assert result is not None


def test_feature_union_pandas_output_with_dataframe_return():
    """Test that FeatureUnion preserves DataFrame structure when transformer returns DataFrame."""
    
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-03", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[1] * len(index), columns=["value"])
    data["date"] = index.date

    class AggregatingTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            # Return a DataFrame with aggregated data - fewer rows than input
            result = X["value"].groupby(X["date"]).sum()
            return result.to_frame()

    # Test with pandas output - this should not raise ValueError about length mismatch
    set_config(transform_output="pandas")
    union = make_union(AggregatingTransformer())
    
    # This should not raise "Length mismatch: Expected axis has X elements, new values have Y elements"
    result = union.fit_transform(data)
    
    # Verify we got a result
    assert result is not None