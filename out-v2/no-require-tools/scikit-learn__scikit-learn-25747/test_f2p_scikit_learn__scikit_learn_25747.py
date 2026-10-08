import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union
import pytest

def test_feature_union_pandas_transform_output_no_index_mismatch_error():
    """Test that FeatureUnion with pandas transform output does not raise 
    ValueError about index length mismatch when transformers return differently shaped data.
    
    This test ensures that the fix for the bug where FeatureUnion would raise
    ValueError: Length mismatch: Expected axis has X elements, new values have Y elements
    when using pandas transform output with transformers that return differently shaped data.
    """
    
    # Create test data with time series that will be grouped
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date

    class GroupByTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            # This returns a DataFrame with fewer rows than the input
            # Group by date, so one row per unique date instead of one per hour
            result = X["value"].groupby(X["date"]).sum()
            return result.to_frame()

    # Test with default output (should work)
    set_config(transform_output="default")
    result_default = make_union(GroupByTransformer()).fit_transform(data)
    
    # Test with pandas output - this should NOT raise ValueError about index mismatch
    set_config(transform_output="pandas")
    
    # The key assertion: this should not raise ValueError about index length mismatch
    try:
        result_pandas = make_union(GroupByTransformer()).fit_transform(data)
        # If we get here without ValueError, it's working correctly
        assert isinstance(result_pandas, pd.DataFrame)
        # The important thing is that it doesn't crash with the specific ValueError
    except ValueError as e:
        if "Length mismatch" in str(e):
            pytest.fail(f"FeatureUnion with pandas transform output failed with index mismatch error: {e}")
        else:
            raise  # Re-raise if it's a different ValueError

def test_feature_union_pandas_transform_output_simple_case():
    """Test that FeatureUnion works with pandas transform output for simple transformers."""
    
    # Create simple test data
    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    class SimpleTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X, y=None):
            # Return a simple DataFrame with same shape
            return pd.DataFrame({"c": X["a"] * 2})

    # Test with default output
    set_config(transform_output="default")
    result_default = make_union(SimpleTransformer()).fit_transform(data)
    
    # Test with pandas output
    set_config(transform_output="pandas")
    result_pandas = make_union(SimpleTransformer()).fit_transform(data)
    
    # Both should work and produce valid results
    assert isinstance(result_pandas, pd.DataFrame)
    assert len(result_pandas) == len(data)