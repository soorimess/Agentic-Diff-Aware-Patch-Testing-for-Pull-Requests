"""
Test for FeatureUnion with pandas transform output and aggregating transformers.

This test reproduces the bug where FeatureUnion fails when using pandas
transform output with a transformer that aggregates data (returns fewer rows
than input). The bug was fixed by changing _wrap_in_pandas_container to not
set the index when data_to_wrap is already a DataFrame.
"""

import pandas as pd
import pytest
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union


class AggregatingTransformer(BaseEstimator, TransformerMixin):
    """Transformer that aggregates data, returning fewer rows than input."""
    
    def fit(self, X: pd.DataFrame, y=None, **kwargs):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        # This transformer aggregates data - groups by date and sums values
        # Returns fewer rows than input (4 dates vs 96 hours)
        result = X["value"].groupby(X["date"]).sum()
        # Return as DataFrame to match expected output format
        return result.to_frame()


def test_feature_union_with_pandas_output_aggregating_transformer():
    """
    Test that FeatureUnion works with pandas transform output and aggregating transformers.
    
    This test should fail with the bug present (before the fix) and pass after the fix.
    """
    # Create test data with 96 hourly observations over 4 days
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # Test with default transform output - should work
    set_config(transform_output="default")
    result_default = make_union(AggregatingTransformer()).fit_transform(data)
    
    # Test with pandas transform output - this should fail with the bug
    set_config(transform_output="pandas")
    
    # This should work after the fix but fails before the fix
    # The error occurs because _wrap_in_pandas_container tries to assign
    # an index with 96 elements to a DataFrame with 4 elements
    try:
        result_pandas = make_union(AggregatingTransformer()).fit_transform(data)
        # If we get here without exception, the fix is working
        assert isinstance(result_pandas, pd.DataFrame)
        # Should have 4 rows (one per unique date)
        assert len(result_pandas) == 4
        assert len(data) == 96
    except ValueError as e:
        if "Length mismatch" in str(e):
            # This is the expected error with the bug present
            pytest.fail("Bug reproduced: Length mismatch when setting index on aggregated DataFrame")
        else:
            raise  # Re-raise if it's a different ValueError


def test_wrap_in_pandas_container_preserves_dataframe_structure():
    """
    Test that _wrap_in_pandas_container preserves DataFrame structure when data_to_wrap is already a DataFrame.
    
    The bug was that when data_to_wrap is a DataFrame and index is provided,
    it would try to assign the index to the DataFrame, causing length mismatch.
    
    After the fix: when data_to_wrap is a DataFrame, it should preserve the DataFrame
    as-is without trying to modify its index.
    """
    # Create test data
    index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
    data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
    data["date"] = index.date
    
    # Create a DataFrame result that simulates what an aggregating transformer returns
    # This has 4 rows (unique dates) vs original data with 96 rows
    transformed_data = data["value"].groupby(data["date"]).sum().to_frame()
    
    # Import the function we're testing
    from sklearn.utils._set_output import _wrap_in_pandas_container
    
    # This should work after the fix - the function should preserve the DataFrame structure
    # and not try to assign an incompatible index
    try:
        result = _wrap_in_pandas_container(
            data_to_wrap=transformed_data,
            columns=None,
            index=data.index  # Original index with 96 elements
        )
        
        # If we get here without error, the fix is working
        # The result should be the same DataFrame (preserved as-is)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4  # Should maintain the aggregated shape
        # The index should be preserved from the original transformed_data, not overwritten
        assert result.index.equals(transformed_data.index)  # Should preserve original index
        
    except ValueError as e:
        if "Length mismatch" in str(e):
            # This is the bug - it's trying to assign the wrong index
            pytest.fail("Bug reproduced: Length mismatch when trying to set index on DataFrame")
        else:
            raise  # Re-raise if it's a different ValueError


def test_wrap_in_pandas_container_with_numpy_array():
    """
    Test that _wrap_in_pandas_container still works correctly with numpy arrays.
    
    This ensures we don't break the normal case where we create a new DataFrame
    from numpy data.
    """
    import numpy as np
    
    # Create numpy array data
    data = np.array([[1, 2], [3, 4], [5, 6]])
    
    # Import the function we're testing
    from sklearn.utils._set_output import _wrap_in_pandas_container
    
    # This should work - creating a new DataFrame from numpy data
    result = _wrap_in_pandas_container(
        data_to_wrap=data,
        columns=['A', 'B'],
        index=['x', 'y', 'z']  # This should be applied to the new DataFrame
    )
    
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 2)
    assert list(result.columns) == ['A', 'B']
    assert list(result.index) == ['x', 'y', 'z']